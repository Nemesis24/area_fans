import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback
from homeassistant.helpers import entity_registry, area_registry, device_registry
from .const import DOMAIN, ATTR_COUNT, ATTR_TOTAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    excluded = entry.data.get("excluded_entities", [])
    
    _LOGGER.debug("Starting Area Fans configuration") 
    _LOGGER.debug(f"Excluded entities: {excluded}")
    
    area_reg = area_registry.async_get(hass)
    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)
    
    areas = area_reg.async_list_areas()
    _LOGGER.debug(f"Found areas: {[area.name for area in areas]}")
    
    sensors = []
    all_fans = set()
    
    for area in areas:
        area_fans = set()
        area_excluded = set()
        
        for entity in entity_reg.entities.values():
            if entity.entity_id.startswith("fan.") and entity.area_id == area.id:
                if entity.entity_id not in excluded:
                    area_fans.add(entity.entity_id)
                    _LOGGER.debug(f"Fan {entity.entity_id} found directly in {area.name}")
                else:
                    area_excluded.add(entity.entity_id)
        
        for device_id in device_reg.devices:
            device = device_reg.async_get(device_id)
            if device and device.area_id == area.id:
                for entity in entity_reg.entities.values():
                    if entity.device_id == device_id and entity.entity_id.startswith("fan."):
                        if entity.entity_id not in excluded:
                            area_fans.add(entity.entity_id)
                            _LOGGER.debug(f"Fan {entity.entity_id} found via device in {area.name}")
                        else:
                            area_excluded.add(entity.entity_id)
        
        if area_fans:
            _LOGGER.debug(f"Area {area.name}: {len(area_fans)} fans found: {area_fans}")
            sensors.append(RoomFansSensor(area.name, list(area_fans), list(area_excluded)))
            all_fans.update(area_fans)

    if all_fans:
        _LOGGER.debug(f"Total fans found: {len(all_fans)}")
        sensors.append(AllFansSensor(list(all_fans), excluded))
    
    _LOGGER.debug(f"Creating {len(sensors)} sensors")
    async_add_entities(sensors)

class RoomFansSensor(SensorEntity):
    def __init__(self, room_name, fans, excluded_fans):
        self._room = room_name
        self._fans = fans
        self._excluded_fans = excluded_fans
        self._attr_name = f"Fans {room_name}"
        self._attr_unique_id = f"area_fans_{room_name.lower().replace(' ', '_')}"
        self._state = STATE_OFF
        self._count = 0
        self._total = len(fans)
        self._fans_on = []
        self._fans_off = []
        _LOGGER.debug(f"Initializing sensor {self._attr_name} with {self._total} fans: {self._fans}")

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:fan" if self._state == STATE_ON else "mdi:fan-off"

    @property
    def extra_state_attributes(self):
        return {
            "count": self._count,
            "of": self._total,
            "count_of": f"{self._count}/{self._total}",
            "fans_on": self._fans_on,
            "fans_off": self._fans_off,
            "excluded_fans": self._excluded_fans,
        }

    async def async_added_to_hass(self):
        @callback
        def async_state_changed(*_):
            self.async_schedule_update_ha_state(True)

        for fan in self._fans:
            self.async_on_remove(
                self.hass.helpers.event.async_track_state_change(
                    fan, async_state_changed
                )
            )
        
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        self._count = 0
        self._fans_on = []
        self._fans_off = []
        
        for fan_id in self._fans:
            state = self.hass.states.get(fan_id)
            if state:
                if state.state == STATE_ON:
                    self._count += 1
                    self._fans_on.append(fan_id)
                else:
                    self._fans_off.append(fan_id)
        
        self._state = STATE_ON if self._count > 0 else STATE_OFF
        _LOGGER.debug(f"Updating {self._attr_name}: {self._count}/{self._total} fans on")

class AllFansSensor(RoomFansSensor):
    def __init__(self, fans, excluded_fans):
        super().__init__("All", fans, excluded_fans)
        self._attr_name = "All Area Fans"
        self._attr_unique_id = "area_fans_all"
