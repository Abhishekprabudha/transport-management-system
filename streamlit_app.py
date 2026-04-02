import streamlit as st
from datetime import datetime
from app.services.repo import TMSRepository
from app.utils.auth import login_panel
from app.utils.styles import inject_styles
from app.utils.kpi import kpi_card, status_badge

st.set_page_config(page_title="TMS Backend Demo", page_icon="🚚", layout="wide")
inject_styles()
repo = TMSRepository()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_panel()
    st.stop()

st.sidebar.title("TMS Backend Demo")
st.sidebar.caption("Operator Control System")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Contracts",
        "Spot Auction",
        "Dispatch Planner",
        "Vehicle Indenting",
        "Tracking Control Tower",
        "E-POD",
        "Freight Settlement",
        "Analytics",
        "Admin",
    ],
)

summary = repo.get_overview_summary()


def render_cursory_task(page_key: str, button_text: str, result_text: str):
    action_key = f"{page_key}_task_ran"
    if st.button(button_text, key=f"{page_key}_task_button"):
        st.session_state[action_key] = True
    if st.session_state.get(action_key):
        st.success(result_text)


if "screen_records" not in st.session_state:
    st.session_state.screen_records = []


def render_record_button(page_label: str):
    record_key = f"{page_label.lower().replace(' ', '_')}_recorded"
    if st.button("Record this screen update", key=f"{record_key}_button"):
        st.session_state.screen_records.append(
            {"Screen": page_label, "Recorded At": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
        )
        st.session_state[record_key] = True
    if st.session_state.get(record_key):
        st.success(f"{page_label} update recorded for overview tracking.")

st.title("Transportation Management System")
st.caption("Unified backend operating layer for planning, execution, monitoring, and analytics")

if page == "Overview":
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        kpi_card("Active Trips", summary["active_trips"], "+12 today")
    with c2:
        kpi_card("Open Auctions", summary["open_auctions"], "Live procurement")
    with c3:
        kpi_card("Open Invoices", summary["open_invoices"], "Pending settlement")
    with c4:
        kpi_card("ePOD Open", summary["open_epod"], "Awaiting closure")
    with c5:
        kpi_card("Transporters", summary["transporters"], "Active network")
    with c6:
        kpi_card("Screen Records", len(st.session_state.screen_records), "Captured from other modules")

    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Operational Backbone")
        st.markdown(
            """
            - Contract lifecycle management
            - Spot procurement and rate discovery
            - Dispatch planning and vehicle assignment
            - Real-time trip monitoring and SLA deviation handling
            - ePOD capture and exception management
            - Freight audit, invoice validation, and settlement
            - KPI cockpit for cost, service, and carrier performance
            """
        )
        st.subheader("Live Alerts")
        for alert in repo.get_alerts():
            st.warning(f"{alert['severity']}: {alert['message']}")
    with right:
        st.subheader("Today’s Dispatch Queue")
        st.dataframe(repo.get_dispatch_table(), use_container_width=True, hide_index=True)
        st.subheader("Recent Screen Records")
        if st.session_state.screen_records:
            st.dataframe(st.session_state.screen_records[-5:], use_container_width=True, hide_index=True)
        else:
            st.info("No screen updates have been recorded yet.")

elif page == "Contracts":
    st.subheader("Vendor Contracts Management")
    render_record_button("Contracts")
    active_contracts = int((repo.get_contracts()["Status"] == "Active").sum())
    render_cursory_task(
        "contracts",
        "Run contract health check",
        f"Health check complete: {active_contracts} active contracts ready for dispatch planning.",
    )
    st.dataframe(repo.get_contracts(), use_container_width=True, hide_index=True)
    st.info("Supports FTL/PTL/Lease contracts, rate card history, SLA tracking, and audit trail.")

elif page == "Spot Auction":
    st.subheader("Spot Auction / RFP Console")
    render_record_button("Spot Auction")
    open_auctions = int((repo.get_auctions()["Status"] == "Open").sum())
    render_cursory_task(
        "spot_auction",
        "Run auction pulse check",
        f"Pulse check complete: {open_auctions} auctions are currently open for bids.",
    )
    st.dataframe(repo.get_auctions(), use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Average Bid Savings", "4.8%", "+0.7%")
    with c2:
        st.metric("Indent Conversion Rate", "82%", "+5%")
    st.caption("Supports live bidding, route-wise price discovery, transporter participation, and post-auction award flow.")

elif page == "Dispatch Planner":
    st.subheader("Dispatch Planning & Load Builder")
    render_record_button("Dispatch Planner")
    in_dispatch = int((repo.get_dispatch_table()["Status"] == "In Dispatch").sum())
    render_cursory_task(
        "dispatch_planner",
        "Run dispatch readiness check",
        f"Readiness check complete: {in_dispatch} load(s) are currently in dispatch stage.",
    )
    st.dataframe(repo.get_dispatch_table(), use_container_width=True, hide_index=True)
    st.markdown("### Load Plan View")
    st.code(repo.get_load_builder_text(), language="text")
    st.caption("Represents load sequencing, vehicle capacity utilization, and stop order logic for demo purposes.")

elif page == "Vehicle Indenting":
    st.subheader("Auto Vehicle Indenting")
    render_record_button("Vehicle Indenting")
    indented = int((repo.get_indents()["Status"] == "Indented").sum())
    render_cursory_task(
        "vehicle_indenting",
        "Run indent availability check",
        f"Availability check complete: {indented} indent(s) are awaiting vehicle confirmation.",
    )
    st.dataframe(repo.get_indents(), use_container_width=True, hide_index=True)
    st.caption("Covers digital requisitioning, ETA visibility, and transporter share-of-business management.")

elif page == "Tracking Control Tower":
    st.subheader("Vehicle Tracking / Control Tower")
    render_record_button("Tracking Control Tower")
    trips = repo.get_trips()
    delayed_trips = int((trips["Status"] == "Delayed").sum())
    render_cursory_task(
        "tracking_control_tower",
        "Run live tracking scan",
        f"Tracking scan complete: {delayed_trips} delayed trip(s) need attention.",
    )
    st.dataframe(trips, use_container_width=True, hide_index=True)
    selected = st.selectbox("Select Trip", trips["Trip ID"].tolist())
    trip = repo.get_trip_details(selected)
    a, b, c, d = st.columns(4)
    a.metric("Trip Status", trip["status"])
    b.metric("ETA", trip["eta_hours"])
    c.metric("Deviation", trip["deviation_km"])
    d.markdown(status_badge(trip["sla_state"]), unsafe_allow_html=True)
    st.json(trip)

elif page == "E-POD":
    st.subheader("Electronic Proof of Delivery")
    render_record_button("E-POD")
    open_epods = int((repo.get_epod()["Status"] == "Open").sum())
    render_cursory_task(
        "epod",
        "Run POD closure check",
        f"Closure check complete: {open_epods} ePOD record(s) are still open.",
    )
    st.dataframe(repo.get_epod(), use_container_width=True, hide_index=True)
    st.caption("Handles consignee confirmation, damage notes, quantity mismatch, and detention event capture.")

elif page == "Freight Settlement":
    st.subheader("Freight Settlement & Audit")
    render_record_button("Freight Settlement")
    pending_invoices = int((repo.get_invoices()["Status"] != "Approved").sum())
    render_cursory_task(
        "freight_settlement",
        "Run settlement audit check",
        f"Audit check complete: {pending_invoices} invoice(s) are pending approval.",
    )
    st.dataframe(repo.get_invoices(), use_container_width=True, hide_index=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Invoice Accuracy", "98.4%", "+1.1%")
    c2.metric("Freight Leakage Prevented", "₹14.2L", "+₹2.1L")
    c3.metric("Approval TAT", "2.8 days", "-0.6 days")

elif page == "Analytics":
    st.subheader("Dashboard & Analytics")
    render_record_button("Analytics")
    top_carrier = repo.get_carrier_kpis().sort_values("On-time", ascending=False).iloc[0]["Carrier"]
    render_cursory_task(
        "analytics",
        "Run KPI spotlight",
        f"KPI spotlight complete: {top_carrier} leads on-time performance in this demo dataset.",
    )
    fig1, fig2 = repo.get_analytics_figures()
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(repo.get_carrier_kpis(), use_container_width=True, hide_index=True)

elif page == "Admin":
    st.subheader("Master Data & System Configuration")
    render_record_button("Admin")
    render_cursory_task(
        "admin",
        "Run master data sanity check",
        "Sanity check complete: core entities are loaded and visible for configuration review.",
    )
    st.markdown(
        """
        **Available backend entities**
        - Plants / warehouses
        - Customers / consignees
        - Transporters
        - Vehicles and capacities
        - Routes and rate cards
        - Shipment orders
        - Contracts and SLAs
        - Users and roles
        - Billing rules and audit controls
        """
    )
    st.dataframe(repo.get_master_snapshot(), use_container_width=True, hide_index=True)
