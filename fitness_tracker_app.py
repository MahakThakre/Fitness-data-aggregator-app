import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

class FitnessTrackerApp:
    def __init__(self):
        self.data = pd.DataFrame()

    def normalize_date(self, date_str):
        """Convert various date formats to YYYY-MM-DD"""
        if pd.isna(date_str):
            return None

        date_str = str(date_str).strip()

        formats = [
            '%Y-%m-%d',      # 2025-09-01
            '%d/%m/%Y',      # 01/09/2025
            '%d-%m-%Y',      # 08-09-2025
            '%m-%d-%Y',      # 09-08-2025
            '%Y/%m/%d',      # 2025/09/01
        ]

        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue

        return None

    def process_uploaded_data(self, csv_file, json_file):
        """Process uploaded files"""
        dfs = []

        if csv_file is not None:
            try:
                csv_data = pd.read_csv(csv_file)
                csv_data['source'] = 'csv'
                dfs.append(csv_data)
                st.success(f"CSV loaded: {len(csv_data)} records")
            except Exception as e:
                st.error(f"Error loading CSV: {e}")

        if json_file is not None:
            try:
                json_data = json.load(json_file)
                json_df = pd.DataFrame(json_data)
                json_df['source'] = 'json'
                dfs.append(json_df)
                st.success(f"JSON loaded: {len(json_df)} records")
            except Exception as e:
                st.error(f"Error loading JSON: {e}")

        if dfs:
            self.data = pd.concat(dfs, ignore_index=True)
            return True
        return False

    def clean_data(self):
        """Clean the merged data"""
        if self.data.empty:
            return

        initial_count = len(self.data)

        # Normalize dates
        self.data['date'] = self.data['date'].apply(self.normalize_date)
        self.data = self.data.dropna(subset=['date'])

        # Convert numeric columns
        numeric_cols = ['steps', 'calories', 'sleep_minutes']
        for col in numeric_cols:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')

        # Remove duplicates
        before_dedup = len(self.data)
        self.data = self.data.drop_duplicates(subset=['date', 'user_id'], keep='first')
        duplicates_removed = before_dedup - len(self.data)

        # Handle missing calories
        if 'calories' in self.data.columns:
            user_avg_calories = self.data.groupby('user_id')['calories'].mean()

            for user_id in self.data['user_id'].unique():
                user_mask = self.data['user_id'] == user_id
                missing_mask = self.data['calories'].isna()
                combined_mask = user_mask & missing_mask

                if combined_mask.any() and user_id in user_avg_calories:
                    avg_cal = user_avg_calories[user_id]
                    if not pd.isna(avg_cal):
                        self.data.loc[combined_mask, 'calories'] = round(avg_cal, 0)

            # Fill remaining with overall average
            overall_avg = self.data['calories'].mean()
            if not pd.isna(overall_avg):
                self.data['calories'] = self.data['calories'].fillna(round(overall_avg, 0))

        return {
            'initial_count': initial_count,
            'final_count': len(self.data),
            'duplicates_removed': duplicates_removed
        }

    def get_week_key(self, date_str):
        """Convert date to week key format"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            week_in_month = ((date_obj.day - 1) // 7) + 1
            return f"{date_obj.year}-{date_obj.month:02d}-week-{week_in_month}"
        except:
            return None

    def compute_user_stats(self):
        """Compute statistics for each user"""
        user_stats = []

        for user_id in self.data['user_id'].unique():
            user_data = self.data[self.data['user_id'] == user_id].copy()

            total_steps = int(user_data['steps'].sum()) if 'steps' in user_data.columns else 0
            total_calories = int(user_data['calories'].sum()) if 'calories' in user_data.columns else 0

            # Weekly averages
            weekly_avg_steps = {}
            user_data.loc[:, 'week_key'] = user_data['date'].apply(self.get_week_key)

            for week_key in user_data['week_key'].dropna().unique():
                week_data = user_data[user_data['week_key'] == week_key]
                avg_steps = int(week_data['steps'].mean()) if 'steps' in week_data.columns else 0
                weekly_avg_steps[week_key] = avg_steps

            user_stats.append({
                'user_id': user_id,
                'total_steps': total_steps,
                'total_calories': total_calories,
                'weekly_avg_steps': weekly_avg_steps
            })

        return user_stats

    def compute_daily_top_user(self):
        """Compute daily top user by steps"""
        daily_top_user = []

        if 'steps' not in self.data.columns:
            return daily_top_user

        for date in self.data['date'].unique():
            day_data = self.data[self.data['date'] == date]
            if not day_data.empty:
                top_user_idx = day_data['steps'].idxmax()
                top_user_row = day_data.loc[top_user_idx]

                daily_top_user.append({
                    'date': date,
                    'user_id': top_user_row['user_id'],
                    'steps': int(top_user_row['steps'])
                })

        daily_top_user.sort(key=lambda x: x['date'])
        return daily_top_user

def main():
    st.set_page_config(
        page_title="Fitness Tracker Data Aggregator",
        page_icon=None,
        layout="wide"
    )

    st.title("Fitness Tracker Data Aggregator")
    st.markdown("Upload your fitness data in CSV and JSON formats for comprehensive analysis!")

    # Sidebar for file uploads
    st.sidebar.header("Data Upload")

    csv_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="CSV file with columns: date, user_id, steps, calories, sleep_minutes"
    )

    json_file = st.sidebar.file_uploader(
        "Upload JSON file", 
        type=['json'],
        help="JSON array with fitness data objects"
    )

    # Use sample data option
    use_sample = st.sidebar.checkbox("Use Sample Data", value=True)

    app = FitnessTrackerApp()

    if use_sample:
        # Load sample data
        try:
            sample_csv = pd.read_csv('sample_data.csv')
            with open('sample_data.json', 'r') as f:
                sample_json = json.load(f)

            app.data = pd.concat([
                sample_csv.assign(source='csv'),
                pd.DataFrame(sample_json).assign(source='json')
            ], ignore_index=True)

            st.sidebar.success("Sample data loaded!")
        except:
            st.sidebar.error("Sample data not found")
    elif csv_file or json_file:
        if app.process_uploaded_data(csv_file, json_file):
            st.success("Data uploaded successfully!")
    else:
        st.info("Please upload CSV and/or JSON files, or use sample data to get started.")
        return

    if app.data.empty:
        st.warning("No data to process. Please upload files or use sample data.")
        return

    # Show raw data
    with st.expander("Raw Data Preview"):
        st.dataframe(app.data.head(10))
        st.write(f"Total records: {len(app.data)}")

    # Process data
    if st.button("Process Data", type="primary"):
        with st.spinner("Processing data..."):
            cleaning_stats = app.clean_data()

            if cleaning_stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Initial Records", cleaning_stats['initial_count'])
                with col2:
                    st.metric("Final Records", cleaning_stats['final_count'])
                with col3:
                    st.metric("Duplicates Removed", cleaning_stats['duplicates_removed'])

            # Compute statistics
            user_stats = app.compute_user_stats()
            daily_top_user = app.compute_daily_top_user()

            # Display results
            st.header("Results")

            # User Statistics
            st.subheader("User Statistics")
            for user in user_stats:
                with st.expander(f"{user['user_id']} Statistics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Steps", f"{user['total_steps']:,}")
                        st.metric("Total Calories", f"{user['total_calories']:,}")
                    with col2:
                        st.write("**Weekly Average Steps:**")
                        for week, avg in user['weekly_avg_steps'].items():
                            st.write(f"{week}: {avg:,} steps")

            # Visualizations
            st.subheader("Data Visualizations")

            # Daily steps chart
            if not app.data.empty:
                fig_daily = px.line(
                    app.data.groupby(['date', 'user_id'])['steps'].sum().reset_index(),
                    x='date', y='steps', color='user_id',
                    title='Daily Steps by User',
                    labels={'steps': 'Steps', 'date': 'Date'}
                )
                st.plotly_chart(fig_daily, use_container_width=True)

                # User totals comparison
                user_totals = pd.DataFrame(user_stats)
                fig_totals = px.bar(
                    user_totals, x='user_id', y='total_steps',
                    title='Total Steps by User',
                    labels={'total_steps': 'Total Steps', 'user_id': 'User'}
                )
                st.plotly_chart(fig_totals, use_container_width=True)

            # Daily top users
            st.subheader("Daily Top Users")
            if daily_top_user:
                df_top = pd.DataFrame(daily_top_user)
                st.dataframe(df_top, use_container_width=True)

                # Top user frequency
                top_user_counts = df_top['user_id'].value_counts()
                fig_top = px.pie(
                    values=top_user_counts.values,
                    names=top_user_counts.index,
                    title='Daily Top User Distribution'
                )
                st.plotly_chart(fig_top, use_container_width=True)

            # Generate output JSON
            output = {
                'user_stats': user_stats,
                'daily_top_user': daily_top_user
            }

            # Download button
            st.subheader("Download Results")
            json_string = json.dumps(output, indent=2)
            st.download_button(
                label="Download JSON Results",
                data=json_string,
                file_name="fitness_results.json",
                mime="application/json"
            )

            # Display JSON
            with st.expander("View JSON Output"):
                st.json(output)

if __name__ == "__main__":
    main()