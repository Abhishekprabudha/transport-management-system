import pandas as pd
import plotly.express as px


class TMSRepository:
    def __init__(self):
        self.contracts = pd.DataFrame([
            ["CTR-101", "ABC Logistics", "Delhi-Mumbai", "FTL", "On Time > 95%", "Active", "2026-12-31"],
            ["CTR-102", "Rapid Haul", "Bengaluru-Hyderabad", "PTL", "POD < 24h", "Active", "2026-10-15"],
            ["CTR-103", "Northline", "Chennai-Kochi", "Lease", "Detention cap", "Under Review", "2026-09-01"],
        ], columns=["Contract ID", "Transporter", "Lane", "Mode", "SLA", "Status", "Expiry"])

        self.auctions = pd.DataFrame([
            ["AUC-9001", "Mumbai-Nagpur", "Open", 7, "₹42,500", "₹39,900", "6.1%"],
            ["AUC-9002", "Delhi-Jaipur", "Awarded", 5, "₹18,200", "₹17,650", "3.0%"],
            ["AUC-9003", "Pune-Surat", "Open", 9, "₹28,100", "₹26,480", "5.8%"],
        ], columns=["Auction ID", "Route", "Status", "Bidders", "Benchmark", "Best Bid", "Savings"])

        self.dispatches = pd.DataFrame([
            ["DSP-3001", "SO-771", "Delhi WH", "Mumbai DC", "32FT MXL", "91%", "Planned", "ABC Logistics"],
            ["DSP-3002", "SO-772", "Pune WH", "Ahmedabad DC", "19FT", "84%", "Assigned", "Rapid Haul"],
            ["DSP-3003", "SO-773", "Chennai WH", "Bengaluru DC", "Container 11T", "88%", "In Dispatch", "SouthWheel"],
        ], columns=["Dispatch ID", "Shipment", "Source", "Destination", "Vehicle", "Utilization", "Status", "Transporter"])

        self.indents = pd.DataFrame([
            ["IND-5501", "Faridabad", "Rama Roadways", "12h", "Indented", "65% SOB"],
            ["IND-5502", "Bhiwandi", "Atlas Movers", "8h", "Assigned", "52% SOB"],
            ["IND-5503", "Hosur", "SouthWheel", "18h", "Rejected", "37% SOB"],
        ], columns=["Indent ID", "Origin", "Transporter", "Reporting ETA", "Status", "Share of Business"])

        self.trips = pd.DataFrame([
            ["TRP-1001", "ABC Logistics", "In Transit", "6.5h", 3.2, "SLA Safe", "Delhi-Mumbai"],
            ["TRP-1002", "Rapid Haul", "Delayed", "9.0h", 11.7, "SLA Risk", "Pune-Ahmedabad"],
            ["TRP-1003", "SouthWheel", "At Destination", "0.5h", 0.0, "Closed", "Chennai-Bengaluru"],
        ], columns=["Trip ID", "Transporter", "Status", "ETA", "Deviation (km)", "SLA State", "Lane"])

        self.epod = pd.DataFrame([
            ["EPOD-001", "TRP-1001", "Open", "Minor carton dent", "0", "Pending"],
            ["EPOD-002", "TRP-1002", "Open", "Quantity mismatch", "2", "Investigate"],
            ["EPOD-003", "TRP-1003", "Closed", "No exception", "0", "Accepted"],
        ], columns=["ePOD ID", "Trip ID", "Status", "Condition Note", "Damage Count", "Resolution"])

        self.invoices = pd.DataFrame([
            ["INV-7001", "ABC Logistics", "TRP-1001", "₹39,900", "Open", "Audit Pending"],
            ["INV-7002", "Rapid Haul", "TRP-1002", "₹17,650", "Pending", "SLA deduction review"],
            ["INV-7003", "SouthWheel", "TRP-1003", "₹26,480", "Approved", "Ready for payment"],
        ], columns=["Invoice ID", "Transporter", "Trip ID", "Amount", "Status", "Audit State"])

        self.carrier_kpis = pd.DataFrame([
            ["ABC Logistics", "96%", "₹2.82", "0.4%", "92%"],
            ["Rapid Haul", "88%", "₹3.11", "1.7%", "80%"],
            ["SouthWheel", "98%", "₹2.66", "0.1%", "95%"],
        ], columns=["Carrier", "On-time", "Cost / km", "Claims Rate", "POD TAT Compliance"])

    def get_overview_summary(self):
        return {
            "active_trips": len(self.trips),
            "open_auctions": int((self.auctions["Status"] == "Open").sum()),
            "open_invoices": int((self.invoices["Status"] != "Approved").sum()),
            "open_epod": int((self.epod["Status"] == "Open").sum()),
            "transporters": self.contracts["Transporter"].nunique(),
        }

    def get_alerts(self):
        return [
            {"severity": "High", "message": "Trip TRP-1002 is in SLA risk due to route deviation."},
            {"severity": "Medium", "message": "Invoice INV-7002 requires deduction review before approval."},
            {"severity": "Low", "message": "Contract CTR-103 is under review and nearing renewal window."},
        ]

    def get_contracts(self):
        return self.contracts

    def get_auctions(self):
        return self.auctions

    def get_dispatch_table(self):
        return self.dispatches

    def get_load_builder_text(self):
        return """Vehicle: 32FT MXL\nCapacity Used: 91%\nStop Sequence:\n1. Delhi WH - Load pharma pallets\n2. Jaipur Crossdock - Partial unload\n3. Mumbai DC - Final unload\n\nLoad Rules Applied:\n- Heavier SKUs placed lower deck\n- Reverse unload sequencing used\n- Temperature-sensitive cartons isolated\n- Fragile material marked in red zone"""

    def get_indents(self):
        return self.indents

    def get_trips(self):
        return self.trips.rename(columns={"Status": "Status", "ETA": "ETA", "Deviation (km)": "Deviation (km)", "SLA State": "SLA State"})

    def get_trip_details(self, trip_id: str):
        row = self.trips[self.trips["Trip ID"] == trip_id].iloc[0]
        return {
            "trip_id": row["Trip ID"],
            "transporter": row["Transporter"],
            "status": row["Status"],
            "eta_hours": row["ETA"],
            "deviation_km": row["Deviation (km)"],
            "sla_state": row["SLA State"],
            "lane": row["Lane"],
            "last_ping": "2026-04-02 11:42",
            "driver": "Assigned Demo Driver",
            "gps_source": "SIM + Fastag + mobile SDK",
            "alerts": ["geofence delay", "route deviation"] if row["Status"] == "Delayed" else ["none"],
        }

    def get_epod(self):
        return self.epod

    def get_invoices(self):
        return self.invoices

    def get_analytics_figures(self):
        fig1 = px.bar(
            pd.DataFrame({"Stage": ["Planned", "In Transit", "Delivered"], "Trips": [12, 31, 18]}),
            x="Stage", y="Trips", title="Trip Stage Distribution"
        )
        fig2 = px.line(
            pd.DataFrame({"Week": ["W1", "W2", "W3", "W4"], "Cost per Ton": [102, 98, 95, 93]}),
            x="Week", y="Cost per Ton", title="Freight Cost Trend"
        )
        return fig1, fig2

    def get_carrier_kpis(self):
        return self.carrier_kpis

    def get_master_snapshot(self):
        return pd.DataFrame([
            ["Plants", 8], ["Customers", 24], ["Transporters", 17], ["Vehicles", 134],
            ["Routes", 46], ["Rate Cards", 61], ["Users", 29], ["SLA Templates", 12]
        ], columns=["Entity", "Count"])
