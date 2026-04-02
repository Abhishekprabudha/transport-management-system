import streamlit as st
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

st.title("Transportation Management System")
st.caption("Unified backend operating layer for planning, execution, monitoring, and analytics")

if page == "Overview":
    c1, c2, c3, c4, c5 = st.columns(5)
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

elif page == "Contracts":
    st.subheader("Vendor Contracts Management")
    st.dataframe(repo.get_contracts(), use_container_width=True, hide_index=True)
    st.info("Supports FTL/PTL/Lease contracts, rate card history, SLA tracking, and audit trail.")

elif page == "Spot Auction":
    st.subheader("Spot Auction / RFP Console")
    st.dataframe(repo.get_auctions(), use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Average Bid Savings", "4.8%", "+0.7%")
    with c2:
        st.metric("Indent Conversion Rate", "82%", "+5%")
    st.caption("Supports live bidding, route-wise price discovery, transporter participation, and post-auction award flow.")

elif page == "Dispatch Planner":
    st.subheader("Dispatch Planning & Load Builder")
    st.dataframe(repo.get_dispatch_table(), use_container_width=True, hide_index=True)
    st.markdown("### Load Plan View")
    st.code(repo.get_load_builder_text(), language="text")
    st.caption("Represents load sequencing, vehicle capacity utilization, and stop order logic for demo purposes.")

elif page == "Vehicle Indenting":
    st.subheader("Auto Vehicle Indenting")
    st.dataframe(repo.get_indents(), use_container_width=True, hide_index=True)
    st.caption("Covers digital requisitioning, ETA visibility, and transporter share-of-business management.")

elif page == "Tracking Control Tower":
    st.subheader("Vehicle Tracking / Control Tower")
    trips = repo.get_trips()
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
    st.dataframe(repo.get_epod(), use_container_width=True, hide_index=True)
    st.caption("Handles consignee confirmation, damage notes, quantity mismatch, and detention event capture.")

elif page == "Freight Settlement":
    st.subheader("Freight Settlement & Audit")
    st.dataframe(repo.get_invoices(), use_container_width=True, hide_index=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Invoice Accuracy", "98.4%", "+1.1%")
    c2.metric("Freight Leakage Prevented", "₹14.2L", "+₹2.1L")
    c3.metric("Approval TAT", "2.8 days", "-0.6 days")

elif page == "Analytics":
    st.subheader("Dashboard & Analytics")
    fig1, fig2 = repo.get_analytics_figures()
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(repo.get_carrier_kpis(), use_container_width=True, hide_index=True)

elif page == "Admin":
    st.subheader("Master Data & System Configuration")
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
