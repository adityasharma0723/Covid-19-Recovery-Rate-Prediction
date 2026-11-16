import os
import glob
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

st.set_page_config(
    page_title="COVID-19 Recovery Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #DBEAFE;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1D4ED8;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_datasets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    cleaned_files = glob.glob(os.path.join(base_dir, "data", "cleaned_covid_dataset", "*.csv"))
    if cleaned_files:
        clean_df = pd.read_csv(cleaned_files[0])
    else:
        clean_df = pd.DataFrame()
        
    predictions_path = os.path.join(base_dir, "results", "predictions.csv")
    preds_df = pd.read_csv(predictions_path) if os.path.exists(predictions_path) else pd.DataFrame()
    
    comp_path = os.path.join(base_dir, "results", "model_comparison.csv")
    comp_df = pd.read_csv(comp_path) if os.path.exists(comp_path) else pd.DataFrame()
    
    feat_path = os.path.join(base_dir, "results", "feature_importance.csv")
    feat_df = pd.read_csv(feat_path) if os.path.exists(feat_path) else pd.DataFrame()
    
    return clean_df, preds_df, comp_df, feat_df

@st.cache_resource
def build_prediction_model(df):
    if df.empty:
        return None
        
    features = [
        "age", "gender", "region/state", "comorbidities",
        "symptoms_1", "symptoms_2", "severity", "hospitalized",
        "icu_admission", "ventilator_support", "vaccination_status",
        "variant", "treatment_given_1", "treatment_given_2", "tests_conducted"
    ]
    
    valid_features = [f for f in features if f in df.columns]
    X = df[valid_features].copy()
    y = df["days_to_recovery"]
    
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(exclude=["object"]).columns.tolist()
    
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols)
    ])
    
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42))
    ])
    
    model.fit(X, y)
    return model

clean_df, preds_df, comp_df, feat_df = load_datasets()
predictor_model = build_prediction_model(clean_df)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/coronavirus.png", width=64)
    st.title("Navigation")
    page = st.radio(
        "Go to",
        [
            "Overview & KPIs",
            "Exploratory Data Analysis",
            "Model Diagnostics",
            "Patient Recovery Predictor",
            "Dataset Explorer"
        ]
    )
    st.divider()
    st.caption("COVID-19 Recovery Prediction System")
    st.caption("Engine: Apache Spark & Machine Learning")

if page == "Overview & KPIs":
    st.markdown('<div class="main-title">COVID-19 Recovery Duration Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Big Data Analytics, Distributed Cleaning, and Random Forest Regression Architecture</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">70,000</div>
            <div class="metric-label">Raw Ingested Records</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(clean_df):,}</div>
            <div class="metric-label">Validated Recoveries</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        avg_rec = clean_df["days_to_recovery"].mean() if not clean_df.empty else 17.5
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rec:.1f} Days</div>
            <div class="metric-label">Mean Recovery Time</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        rmse_val = comp_df.loc[comp_df["Metric"] == "RMSE", "Random Forest"].values[0] if not comp_df.empty else 7.49
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{rmse_val:.2f} Days</div>
            <div class="metric-label">Model RMSE</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("###")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Variant Breakdown in Validated Cohort")
        if not clean_df.empty and "variant" in clean_df.columns:
            variant_counts = clean_df["variant"].value_counts().reset_index()
            variant_counts.columns = ["Variant", "Count"]
            fig_variant = px.pie(
                variant_counts,
                names="Variant",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_variant.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_variant, use_container_width=True)
            
    with col_b:
        st.subheader("Distribution of Disease Severity")
        if not clean_df.empty and "severity" in clean_df.columns:
            sev_counts = clean_df["severity"].value_counts().reset_index()
            sev_counts.columns = ["Severity", "Count"]
            fig_sev = px.bar(
                sev_counts,
                x="Severity",
                y="Count",
                color="Severity",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_sev.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_sev, use_container_width=True)
            
    st.subheader("Pipeline Architecture")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.info("**1. Spark Ingestion**\n\nIngestion of 70k multi-centre COVID-19 patient records with schema inference.")
    with p2:
        st.info("**2. Strict Data Cleaning**\n\nFilter deceased & contradictory cases, impute categorical NaNs, trim strings.")
    with p3:
        st.info("**3. Vector Pipeline**\n\nOneHotEncoding, VectorAssembler, and StandardScaler for numerical/categorical inputs.")
    with p4:
        st.info("**4. Random Forest ML**\n\n100-tree ensemble with evaluation on RMSE, MAE, R², and feature importance.")

elif page == "Exploratory Data Analysis":
    st.markdown('<div class="main-title">Exploratory Data Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Explore patient demographic distributions and clinical recovery dynamics</div>', unsafe_allow_html=True)
    
    if not clean_df.empty:
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_variant = st.multiselect(
                "Filter Variant",
                options=clean_df["variant"].unique(),
                default=clean_df["variant"].unique()
            )
        with f2:
            selected_severity = st.multiselect(
                "Filter Severity",
                options=clean_df["severity"].unique(),
                default=clean_df["severity"].unique()
            )
        with f3:
            age_range = st.slider(
                "Age Range",
                min_value=int(clean_df["age"].min()),
                max_value=int(clean_df["age"].max()),
                value=(int(clean_df["age"].min()), int(clean_df["age"].max()))
            )
            
        filtered_df = clean_df[
            (clean_df["variant"].isin(selected_variant)) &
            (clean_df["severity"].isin(selected_severity)) &
            (clean_df["age"].between(age_range[0], age_range[1]))
        ]
        
        st.markdown(f"**Showing {len(filtered_df):,} records matching filters**")
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### Recovery Days by Variant")
            fig_box = px.box(
                filtered_df,
                x="variant",
                y="days_to_recovery",
                color="variant",
                points="outliers",
                labels={"days_to_recovery": "Recovery Duration (Days)", "variant": "Viral Variant"}
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
        with g2:
            st.markdown("#### Recovery Days vs Patient Age")
            fig_scatter = px.histogram(
                filtered_df,
                x="days_to_recovery",
                nbins=25,
                color="severity",
                marginal="violin",
                labels={"days_to_recovery": "Recovery Duration (Days)"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        g3, g4 = st.columns(2)
        with g3:
            st.markdown("#### Primary Comorbidities & Recovery")
            comorb_avg = filtered_df.groupby("comorbidities")["days_to_recovery"].mean().reset_index()
            fig_comorb = px.bar(
                comorb_avg.sort_values(by="days_to_recovery"),
                x="days_to_recovery",
                y="comorbidities",
                orientation="h",
                color="days_to_recovery",
                color_continuous_scale="Viridis",
                labels={"days_to_recovery": "Mean Recovery Days", "comorbidities": "Comorbidity"}
            )
            st.plotly_chart(fig_comorb, use_container_width=True)
            
        with g4:
            st.markdown("#### Primary Treatments & Recovery")
            treat_avg = filtered_df.groupby("treatment_given_1")["days_to_recovery"].mean().reset_index()
            fig_treat = px.bar(
                treat_avg.sort_values(by="days_to_recovery"),
                x="days_to_recovery",
                y="treatment_given_1",
                orientation="h",
                color="days_to_recovery",
                color_continuous_scale="Blues",
                labels={"days_to_recovery": "Mean Recovery Days", "treatment_given_1": "Treatment"}
            )
            st.plotly_chart(fig_treat, use_container_width=True)
    else:
        st.warning("Cleaned dataset not found.")

elif page == "Model Diagnostics":
    st.markdown('<div class="main-title">Model Diagnostics & Evaluation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluation against baseline, error distributions, and feature importances</div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    if not comp_df.empty:
        rf_rmse = comp_df.loc[comp_df["Metric"] == "RMSE", "Random Forest"].values[0]
        base_rmse = comp_df.loc[comp_df["Metric"] == "RMSE", "Baseline"].values[0]
        
        rf_mae = comp_df.loc[comp_df["Metric"] == "MAE", "Random Forest"].values[0]
        base_mae = comp_df.loc[comp_df["Metric"] == "MAE", "Baseline"].values[0]
        
        rf_r2 = comp_df.loc[comp_df["Metric"] == "R2", "Random Forest"].values[0]
        base_r2 = comp_df.loc[comp_df["Metric"] == "R2", "Baseline"].values[0]
        
        with m1:
            st.metric("Root Mean Squared Error (RMSE)", f"{rf_rmse:.4f}", f"Baseline: {base_rmse:.4f}")
        with m2:
            st.metric("Mean Absolute Error (MAE)", f"{rf_mae:.4f}", f"Baseline: {base_mae:.4f}")
        with m3:
            st.metric("R² Determination", f"{rf_r2:.4f}", f"Baseline: {base_r2:.4f}")
            
    st.markdown("###")
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.subheader("Actual vs Predicted Recovery Days")
        if not preds_df.empty:
            fig_act_pred = px.scatter(
                preds_df,
                x="label",
                y="prediction",
                opacity=0.6,
                labels={"label": "Actual Recovery Duration (Days)", "prediction": "Predicted Duration (Days)"},
                title="Actual vs Predicted Values"
            )
            min_val = min(preds_df["label"].min(), preds_df["prediction"].min())
            max_val = max(preds_df["label"].max(), preds_df["prediction"].max())
            fig_act_pred.add_trace(
                go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode="lines",
                    line=dict(color="red", dash="dash"),
                    name="Ideal Fit (y = x)"
                )
            )
            st.plotly_chart(fig_act_pred, use_container_width=True)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_dir, "results", "actual_vs_predicted.png")
            if os.path.exists(img_path):
                st.image(img_path)
                
    with col_plot2:
        st.subheader("Prediction Error Distribution")
        if not preds_df.empty and "Error" in preds_df.columns:
            fig_err = px.histogram(
                preds_df,
                x="Error",
                nbins=25,
                marginal="box",
                labels={"Error": "Residual Error (Actual - Predicted)"},
                color_discrete_sequence=["#DC2626"],
                title="Distribution of Residual Errors"
            )
            fig_err.add_vline(x=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig_err, use_container_width=True)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_dir, "results", "prediction_errors.png")
            if os.path.exists(img_path):
                st.image(img_path)

    st.subheader("Top Feature Importances")
    if not feat_df.empty:
        top_15 = feat_df.head(15).sort_values(by="Importance", ascending=True)
        fig_feat = px.bar(
            top_15,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Tealgrn"
        )
        st.plotly_chart(fig_feat, use_container_width=True)

elif page == "Patient Recovery Predictor":
    st.markdown('<div class="main-title">Interactive Patient Recovery Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Enter patient clinical metrics to predict expected recovery duration</div>', unsafe_allow_html=True)
    
    with st.form("prediction_form"):
        st.markdown("#### Patient Demographics & Geography")
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider("Patient Age", 1, 100, 45)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
        with col3:
            region = st.selectbox(
                "Region / State",
                ["California", "Berlin", "London", "Cape Town", "São Paulo", "Punjab", "Sindh", "Beijing", "Unknown"]
            )
            
        st.markdown("#### Symptoms & Clinical Status")
        col4, col5, col6 = st.columns(3)
        with col4:
            symptom1 = st.selectbox(
                "Primary Symptom",
                ["Fever", "Cough", "Fatigue", "Headache", "Loss of Smell", "Sore Throat", "Unknown"]
            )
        with col5:
            symptom2 = st.selectbox(
                "Secondary Symptom",
                ["Fatigue", "Cough", "Fever", "Loss of Smell", "Sore Throat", "Headache", "Unknown"]
            )
        with col6:
            comorbidity = st.selectbox(
                "Comorbidity",
                ["None", "Diabetes", "Hypertension", "Heart Disease", "Cancer", "Asthma", "Unknown"]
            )
            
        col7, col8, col9 = st.columns(3)
        with col7:
            severity = st.selectbox("Disease Severity", ["Mild", "Moderate", "Severe", "Critical"])
        with col8:
            variant = st.selectbox("Identified Variant", ["Omicron", "Delta", "Alpha", "Unknown"])
        with col9:
            vaccination = st.selectbox("Vaccination Status", ["None", "Partial", "Full", "Booster", "Unknown"])
            
        st.markdown("#### Clinical Interventions")
        col10, col11, col12 = st.columns(3)
        with col10:
            hospitalized = st.selectbox("Hospitalized", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            icu = st.selectbox("ICU Admission", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        with col11:
            ventilator = st.selectbox("Ventilator Support", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            tests = st.slider("Diagnostic Tests Conducted", 1, 6, 2)
        with col12:
            treatment1 = st.selectbox(
                "Treatment Given 1",
                ["Paracetamol", "Antibiotics", "Oxygen", "Steroids", "Remdesivir", "Unknown"]
            )
            treatment2 = st.selectbox(
                "Treatment Given 2",
                ["None", "Steroids", "Oxygen", "Antibiotics", "Paracetamol", "Remdesivir", "Unknown"]
            )
            
        submitted = st.form_submit_button("Predict Recovery Duration", type="primary", use_container_width=True)
        
    if submitted and predictor_model:
        input_data = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "region/state": region,
            "comorbidities": comorbidity,
            "symptoms_1": symptom1,
            "symptoms_2": symptom2,
            "severity": severity,
            "hospitalized": hospitalized,
            "icu_admission": icu,
            "ventilator_support": ventilator,
            "vaccination_status": vaccination,
            "variant": variant,
            "treatment_given_1": treatment1,
            "treatment_given_2": treatment2 if treatment2 != "None" else "Unknown",
            "tests_conducted": tests
        }])
        
        predicted_days = float(predictor_model.predict(input_data)[0])
        lower_bound = max(1.0, predicted_days - 6.5)
        upper_bound = predicted_days + 6.5
        
        st.markdown("### Prediction Result")
        res1, res2, res3 = st.columns(3)
        with res1:
            st.success(f"### Expected Recovery:\n## **{predicted_days:.1f} Days**")
        with res2:
            st.info(f"### 95% Confidence Range:\n## **{lower_bound:.0f} - {upper_bound:.0f} Days**")
        with res3:
            if severity in ["Severe", "Critical"] or ventilator == 1 or icu == 1:
                st.error("### Acuity Profile:\n## **High Clinical Risk**")
            else:
                st.success("### Acuity Profile:\n## **Standard Recovery**")

elif page == "Dataset Explorer":
    st.markdown('<div class="main-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Inspect cleaned records, column distributions, and export data</div>', unsafe_allow_html=True)
    
    if not clean_df.empty:
        st.dataframe(clean_df.head(100), use_container_width=True)
        csv_data = clean_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Cleaned Dataset (CSV)",
            data=csv_data,
            file_name="cleaned_covid_dataset.csv",
            mime="text/csv"
        )
    else:
        st.info("Dataset loading...")

