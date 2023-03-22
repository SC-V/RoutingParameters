import json
import streamlit as st

st.markdown(f"# Get routing parameters")
st.warning(f"Specify parameters below, then copy-paste them to /manual-routing in tariff editor. Need to add new sorting center? Ask in the SC chat!", icon="⚠️")

country = st.selectbox('Country', ["Mexico", "Chile", "UAE"], index=0, help='Defines a timezone used for routing')
country_timezones = {
    "Mexico": "-06:00",
    "Chile": "-03:00",
    "UAE": "+03:00",
    "Turkey (Vize Test)": "+03:00"
}
country_sorting_centers = {
    "Mexico": "mexico sc",
    "Chile": "chile sc",
    "UAE": "Dubai sc",
    "Turkey (Vize Test)": "vize sc test"
}
country_timezone = country_timezones[country]
sorting_center = country_sorting_centers[country]

interval_start, interval_end = st.select_slider(
    'Select delivery window',
    options=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
             '22', '23', '24'],
    value=('00', '24'))

deliver_till = f"1970-01-02T00:00:00{country_timezone}" if interval_end == '24' else f"1970-01-01T{interval_end}:00:00{country_timezone}"
start_routing_at = f"1970-01-02T00:00:00{country_timezone}" if interval_start == '24' else f"1970-01-01T{interval_start}:00:00{country_timezone}"
pickup_till = start_routing_at

col_cour, col_unit, col_prox = st.columns(3, gap="medium")
with col_cour:
    couriers = st.number_input('Maximum number of couriers', value=10, min_value=0, max_value=3000, step=1)
with col_unit:
    units = st.number_input('Limit of orders per courier', value=35, min_value=0, max_value=500, step=1)
with col_prox:
    global_proximity_factor = st.number_input('Proximity factor', value=0.3, min_value=0.0, max_value=10.0, step=0.1)

col_qual, col_excl = st.columns(2, gap="medium")
with col_qual:
    quality = st.selectbox('Routing quality', ["normal", "low", "high"], index=0, help='Higher the quality, longer the routing time')
with col_excl:
    excluded_list = st.text_area('Claims to exclude from routing', height=200, help='Copy and paste from the route reports app if you need to exclude claims from routing')
    if excluded_list:
        excluded_list = excluded_list.split()

st.write('Delivery window from', interval_start, 'to', interval_end, f"{country} time (GMT{country_timezone}) –",
         str(int(interval_end) - int(interval_start)), f"hours, .\n",
         "Routing for no more than", str(couriers), "couriers, with maximum parcels per courier of", str(units))

routing_parameters = {
    "group_id": sorting_center,
    "routing_settings_overrides": {
        "quality": quality,
        "delivery_guarantees": {
            "start_routing_at": start_routing_at,
            "pickup_till": pickup_till,
            "deliver_till": deliver_till
        },
        "copy_fake_courier": {
            "count": couriers,
            "courier_pattern": {"units": units}
        },
        "global_proximity_factor": global_proximity_factor
    }
}

if excluded_list:
    routing_parameters["excluded_claims"] = excluded_list

routing_parameters = json.dumps(routing_parameters, indent=2)
st.code(routing_parameters, language="json")

if st.button("Celebrate shipment!"):
    st.balloons()

