import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.stats import gaussian_kde
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, "daily_gym_attendance_workout_data.csv")
OUT_DIR = os.path.join(PROJECT_ROOT, "media", "generated")

os.makedirs(OUT_DIR, exist_ok=True)

def energy_density_flow():
    df = pd.read_csv(DATA_PATH)

    x = df["workout_duration_minutes"].values
    y = df["calories_burned"].values

    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    plt.style.use("dark_background")
    plt.figure(figsize=(10, 7))
    sc = plt.scatter(x, y, c=z, s=25, cmap="viridis", alpha=0.85)
    plt.title("Energy Density Flow")
    plt.xlabel("Workout Duration")
    plt.ylabel("Calories Burned")
    plt.colorbar(sc, label="Density")

    path = os.path.join(OUT_DIR, "energy_density.png")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

    return "generated/energy_density.png"


def weekly_heatmap():
    df = pd.read_csv(DATA_PATH)
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    df["check_in_time"] = pd.to_datetime(df["check_in_time"], format="%H:%M", errors="coerce")

    df["weekday"] = df["visit_date"].dt.dayofweek
    df["hour"] = df["check_in_time"].dt.hour

    matrix = df.pivot_table(index="weekday", columns="hour",
                            values="workout_duration_minutes",
                            aggfunc="mean", fill_value=0)

    matrix = matrix.reindex(index=range(7), columns=range(24), fill_value=0)
    smooth = gaussian_filter(matrix.values, sigma=1.2)

    plt.style.use("dark_background")
    plt.figure(figsize=(11, 6))
    plt.imshow(smooth, aspect="auto", cmap="plasma", interpolation="bicubic")
    plt.yticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    plt.xticks(range(0, 24, 3), [f"{h}h" for h in range(0, 24, 3)])
    plt.title("Weekly Energy Matrix")
    plt.colorbar(label="Intensity")

    path = os.path.join(OUT_DIR, "weekly_heatmap.png")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

    return "generated/weekly_heatmap.png"
def seasonal_workout_mandala():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    DATA_PATH = os.path.join(BASE_DIR, "daily_gym_attendance_workout_data.csv")
    OUT_DIR = os.path.join(PROJECT_ROOT, "media", "generated")
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    df["month"] = df["visit_date"].dt.month

    pivot = df.pivot_table(
        index="month",
        columns="workout_type",
        values="workout_duration_minutes",
        aggfunc="sum",
        fill_value=0
    ).reindex(range(1, 13), fill_value=0)

    months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(9, 9))
    ax = plt.subplot(111, polar=True)

    bottom = np.zeros(12)
    colors = {
        "HIIT": "#ff5f87",
        "Strength Training": "#b24b6a",
        "Cardio": "#4f46e5",
        "CrossFit": "#f59e0b",
        "Yoga": "#14b8a6"
    }

    for workout in pivot.columns:
        values = pivot[workout].values
        ax.bar(
            angles,
            values,
            width=2*np.pi/12 * 0.9,
            bottom=bottom,
            label=workout,
            color=colors.get(workout, None),
            edgecolor="white",
            linewidth=0.5,
            alpha=0.9
        )
        bottom += values

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles), months_labels)
    ax.set_title("Seasonal Workout Mandala", fontsize=18, pad=20)
    fig.text(
    0.5, 0.05, 
    "Numbers mean the total of exercise minutes for that month (all exercises combined)",
    ha="center",
    fontsize=12,
    color="white",
    alpha=0.9
)
    ax.grid(color="white", alpha=0.1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

    path = os.path.join(OUT_DIR, "seasonal_mandala.png")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

    return "generated/seasonal_mandala.png"


def interactive_bubble_chart():
    import pandas as pd
    import plotly.express as px
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    DATA_PATH = os.path.join(BASE_DIR, "daily_gym_attendance_workout_data.csv")
    OUT_DIR = os.path.join(PROJECT_ROOT, "frontend", "static", "plots")
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    fig = px.scatter(
        df, 
        x="workout_duration_minutes", 
        y="calories_burned",
        size="age", 
        color="workout_type",
        hover_name="member_id",
        template="plotly_dark",
        title="Gym Performance Analysis: Duration vs Calories (Interactive)",
        hover_data={
            "workout_duration_minutes": ':.1f',
            "calories_burned": ':.0f',
            "age": True,
            "gender": True,
            "attendance_status": True,
            "membership_type": True
        }
    )

    path = os.path.join(OUT_DIR, "bubble_chart.html")
    fig.write_html(path)

    return "plots/bubble_chart.html"


def interactive_sunburst():
    import pandas as pd
    import plotly.express as px
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    DATA_PATH = os.path.join(BASE_DIR, "daily_gym_attendance_workout_data.csv")
    OUT_DIR = os.path.join(PROJECT_ROOT, "frontend", "static", "plots")
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    fig = px.sunburst(
        df,
        path=['membership_type', 'gender', 'workout_type'], 
        values='calories_burned',
        color='workout_type',
        title="Interactive Gym Member Segmentation",
        template="plotly_dark"
    )

    fig.update_traces(
        hovertemplate='<b>Category:</b> %{label}<br><b>Total Calories:</b> %{value}<br><b>Parent:</b> %{parent}'
    )

    path = os.path.join(OUT_DIR, "sunburst.html")
    fig.write_html(path)

    return "plots/sunburst.html"
