import json
import streamlit as st

st.markdown(f"# Orders load and routing")
st.subheader("Get routing parameters", anchor=None)

interval_start, interval_end = st.select_slider(
    'Select delivery window',
    options=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
             '22', '23', '24'],
    value=('00', '24'))

deliver_till = "1970-01-02T00:00:00-03:00" if interval_end == '24' else f"1970-01-01T{interval_end}:00:00-03:00"
start_routing_at = "1970-01-02T00:00:00-03:00" if interval_start == '24' else f"1970-01-01T{interval_start}:00:00-03:00"
pickup_till = start_routing_at

col_cour, col_unit, col_prox = st.columns(3, gap="medium")
with col_cour:
    couriers = st.number_input('Maximum number of couriers', value=10, min_value=0, max_value=3000, step=1)
with col_unit:
    units = st.number_input('Limit of orders per courier', value=50, min_value=0, max_value=500, step=1)
with col_prox:
    global_proximity_factor = st.number_input('Proximity factor', value=0.0, min_value=0.0, max_value=10.0, step=0.1)

col_qual, col_excl = st.columns(2, gap="medium")
with col_qual:
    quality = st.selectbox('Routing quality', ["normal", "low", "high"], index=0, help='Higher the quality, longer the routing time')
with col_excl:
    excluded_list = st.text_area('Claims to exclude from routing', height=200, help='Copy and paste from the route reports app if you need to exclude claims from routing')
    if excluded_list:
        excluded_list = orders_list.split()

st.write('Delivery window from', interval_start, 'to', interval_end, "–",
         str(int(interval_end) - int(interval_start)), "hours, Chile time (GMT-3).\n",
         "Routing for no more than", str(couriers), "couriers, with maximum parcels per courier of", str(units))

routing_parameters = {
    "group_id": "mexico sc",
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
