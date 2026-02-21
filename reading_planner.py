import streamlit as st
from datetime import datetime, timedelta
import math


# Translation dictionary
TRANSLATIONS = {
    "ro": {
        "page_title": "📚 Plan de Lectură",
        "description": "Creează un plan personalizat pentru a termina cartea ta la timp!",
        "book_pages": "📖 Total pagini carte:",
        "weeks": "📅 Număr de săptămâni:",
        "days_per_week": "🗓️ Zile de citit pe săptămână:",
        "start_date": "🚀 Data de începere:",
        "reading_days": "📆 Zilele în care citești:",
        "intensity_section": "⚡ Intensitate citit",
        "intensity_help": "Ajustează cât citești în fiecare zi (100% = normal)",
        "preview": "📊 Previzualizare:",
        "generate_button": "✨ Generează Plan",
        "daily_goal": "Citește zilnic:",
        "weekly_goal": "Citește săptămânal:",
        "reading_plan": "📖 Planul Tău de Lectură pe",
        "days": "zile",
        "week": "SĂPTĂMÂNA",
        "day": "Zi",
        "pages": "p.",
        "to_page": "până la pag.",
        "goal": "Obiectiv:",
        "language_selector": "🌍 Alege limba / Choose language:",
        "day_names": {
            "long": {
                0: "🌟Duminică",
                1: "Luni",
                2: "Marți",
                3: "Miercuri",
                4: "Joi",
                5: "Vineri",
                6: "🌟Sâmbătă",
            },
            "short": {
                0: "🌟Dum.",
                1: "Lun.",
                2: "Mar.",
                3: "Mie.",
                4: "Joi",
                5: "Vin.",
                6: "🌟Sâm.",
            },
        },
        "select_days": "Selectează cel puțin o zi!",
    },
    "en": {
        "page_title": "📚 Reading Planner",
        "description": "Create a personalized plan to finish your book on time!",
        "book_pages": "📖 Total book pages:",
        "weeks": "📅 Number of weeks:",
        "days_per_week": "🗓️ Reading days per week:",
        "start_date": "🚀 Start date:",
        "reading_days": "📆 Days you'll read:",
        "intensity_section": "⚡ Reading Intensity",
        "intensity_help": "Adjust how much you read each day (100% = normal)",
        "preview": "📊 Preview:",
        "generate_button": "✨ Generate Plan",
        "daily_goal": "Read daily:",
        "weekly_goal": "Read weekly:",
        "reading_plan": "📖 Your Reading Plan for",
        "days": "days",
        "week": "WEEK",
        "day": "Day",
        "pages": "p.",
        "to_page": "to page",
        "goal": "Goal:",
        "language_selector": "🌍 Alege limba / Choose language:",
        "day_names": {
            "long": {
                0: "🌟Sunday",
                1: "Monday",
                2: "Tuesday",
                3: "Wednesday",
                4: "Thursday",
                5: "Friday",
                6: "🌟Saturday",
            },
            "short": {
                0: "🌟Sun.",
                1: "Mon.",
                2: "Tue.",
                3: "Wed.",
                4: "Thu.",
                5: "Fri.",
                6: "🌟Sat.",
            },
        },
        "select_days": "Please select at least one day!",
    }
}


def get_day_name(date: datetime, lang: str, short: bool = False) -> str:
    """
    Get the localized day name for a given date.

    Args:
        date (datetime): The date object
        lang (str): Language code ('ro' or 'en')
        short (bool): Return short version (2 letters)

    Returns:
        str: Localized day name
    """
    ro_long = TRANSLATIONS["ro"]["day_names"]["long"]
    en_long = TRANSLATIONS["en"]["day_names"]["long"]
    ro_short = TRANSLATIONS["ro"]["day_names"]["short"]
    en_short = TRANSLATIONS["en"]["day_names"]["short"]

    custom_index = (date.weekday() + 1) % 7

    days = {
        0: {"ro": ro_long[0], "en": en_long[0], "ro_short": ro_short[0], "en_short": en_short[0]},
        1: {"ro": ro_long[1], "en": en_long[1], "ro_short": ro_short[1], "en_short": en_short[1]},
        2: {"ro": ro_long[2], "en": en_long[2], "ro_short": ro_short[2], "en_short": en_short[2]},
        3: {"ro": ro_long[3], "en": en_long[3], "ro_short": ro_short[3], "en_short": en_short[3]},
        4: {"ro": ro_long[4], "en": en_long[4], "ro_short": ro_short[4], "en_short": en_short[4]},
        5: {"ro": ro_long[5], "en": en_long[5], "ro_short": ro_short[5], "en_short": en_short[5]},
        6: {"ro": ro_long[6], "en": en_long[6], "ro_short": ro_short[6], "en_short": en_short[6]},
    }
    key = f"{lang}_short" if short else lang
    return days[custom_index][key]


def get_month_name(month: int, lang: str) -> str:
    """
    Get the localized month abbreviation.

    Args:
        month (int): Month number (1-12)
        lang (str): Language code ('ro' or 'en')

    Returns:
        str: Localized month abbreviation
    """
    months = {
        1: {"ro": "ian.", "en": "Jan."},
        2: {"ro": "feb.", "en": "Feb."},
        3: {"ro": "mar.", "en": "Mar."},
        4: {"ro": "apr.", "en": "Apr."},
        5: {"ro": "mai", "en": "May"},
        6: {"ro": "iun.", "en": "Jun."},
        7: {"ro": "iul.", "en": "Jul."},
        8: {"ro": "aug.", "en": "Aug."},
        9: {"ro": "sep.", "en": "Sep."},
        10: {"ro": "oct.", "en": "Oct."},
        11: {"ro": "noi.", "en": "Nov."},
        12: {"ro": "dec.", "en": "Dec."},
    }
    return months[month][lang]


def format_date(date: datetime, lang: str, short_day: bool = False) -> str:
    """
    Format date as "Tuesday, 05 Aug 2025" or "Ma, 05 Aug 2025" (short version).

    Args:
        date (datetime): The date to format
        lang (str): Language code ('ro' or 'en')
        short_day (bool): Use short day name (2 letters)

    Returns:
        str: Formatted date string
    """
    day_name = get_day_name(date, lang, short=short_day)
    month_name = get_month_name(date.month, lang)
    return f"{day_name}, {date.day:02d} {month_name} {date.year}"


def generate_reading_dates(start_date: datetime, selected_weekdays: list, total_reading_days: int) -> list:
    """
    Generate a list of actual reading dates based on selected weekdays.

    Args:
        start_date (datetime): Starting date
        selected_weekdays (list): List of selected weekday indices (0=Monday, 6=Sunday)
        total_reading_days (int): Total number of reading days needed

    Returns:
        list: List of datetime objects for reading days
    """
    reading_dates = []
    current_date = start_date

    python_weekdays = [(day - 1) % 7 for day in selected_weekdays]

    while len(reading_dates) < total_reading_days:
        if current_date.weekday() in python_weekdays:
            reading_dates.append(current_date)
        current_date += timedelta(days=1)

    return reading_dates


def calculate_pages_per_day(total_pages: int, total_reading_days: int, intensities: dict, selected_days: list) -> dict:
    """
    Calculate pages per day based on intensity percentages.

    Args:
        total_pages (int): Total book pages
        total_reading_days (int): Total number of reading days
        intensities (dict): Dictionary with weekday as key and intensity (0-200) as value
        selected_days (list): List of selected weekdays

    Returns:
        dict: Dictionary with weekday as key and pages to read per occurrence as value
    """
    # Calculate how many times each day appears in the total schedule
    weeks = total_reading_days / len(selected_days)

    # Calculate total "intensity units" across ALL reading days
    total_intensity_units = sum(intensities[day] for day in selected_days) * weeks

    # Calculate pages per intensity unit
    pages_per_unit = total_pages / total_intensity_units

    # Calculate pages for each day type
    pages_per_day = {}
    for day in selected_days:
        pages_per_day[day] = pages_per_unit * intensities[day]

    return pages_per_day


def main() -> None:
    """
    Main Streamlit interface for the reading plan generator with Romanian and English support.
    """
    # Language selector
    lang = st.selectbox(
        TRANSLATIONS["en"]["language_selector"],
        options=["en", "ro"],
        format_func=lambda x: "English" if x == "en" else "Română",
        index=0
    )

    t = TRANSLATIONS[lang]

    st.title(t["page_title"])
    st.write(t["description"])

    # Input fields
    col1, col2 = st.columns(2)

    with col1:
        book_pages = st.number_input(t["book_pages"], min_value=1, value=300, step=1)
        weeks = st.number_input(t["weeks"], min_value=1, value=4, step=1)

    with col2:
        start_date = st.date_input(t["start_date"], value=datetime.today())
        start_date = datetime.combine(start_date, datetime.min.time())

    # Day selection
    st.write(t["reading_days"])
    day_cols = st.columns(7)

    days = TRANSLATIONS[lang]["day_names"]["short"]
    weekday_names = [days[0], days[1], days[2], days[3], days[4], days[5], days[6]]

    selected_days = []
    for i, (col, day_name) in enumerate(zip(day_cols, weekday_names)):
        with col:
            if st.checkbox(day_name, value=(1 <= i <= 5), key=f"day_{i}"):
                selected_days.append(i)

    # Intensity sliders
    if selected_days:
        st.markdown(f"### {t['intensity_section']}")
        st.caption(t['intensity_help'])

        intensities = {}
        intensity_cols = st.columns(len(selected_days))

        for idx, (col, day_idx) in enumerate(zip(intensity_cols, selected_days)):
            with col:
                day_name = weekday_names[day_idx]
                intensity = st.slider(
                    day_name,
                    min_value=50,
                    max_value=200,
                    value=100,
                    step=10,
                    key=f"intensity_{day_idx}",
                    label_visibility="visible"
                )
                intensities[day_idx] = intensity

        # Preview calculation
        days_per_week = len(selected_days)
        total_reading_days = weeks * days_per_week
        preview_pages_distribution = calculate_pages_per_day(book_pages, total_reading_days, intensities, selected_days)
        preview_parts = []

        for day_idx in selected_days:
            day_name_short = weekday_names[day_idx]
            pages = preview_pages_distribution[day_idx]
            preview_parts.append(f"{day_name_short}: {math.ceil(pages)} {t['pages']}")

        st.info(f"{t['preview']} {' | '.join(preview_parts)}")

    if st.button(t["generate_button"], type="primary"):
        if not selected_days:
            st.error(t["select_days"])
            return

        days_per_week = len(selected_days)
        total_reading_days = weeks * days_per_week

        # Calculate pages per day based on intensities
        pages_distribution = calculate_pages_per_day(book_pages, total_reading_days, intensities, selected_days)

        # Calculate average for display
        avg_pages_per_day = book_pages / total_reading_days
        pages_per_week = book_pages / weeks

        # Generate actual reading dates
        reading_dates = generate_reading_dates(start_date, selected_days, total_reading_days)

        # Display goals
        st.success(f"{t['daily_goal']} **~{int(avg_pages_per_day)} {t['pages']}**")
        st.info(f"{t['weekly_goal']} **{int(pages_per_week)} {t['pages']}**")

        st.markdown(f"### {t['reading_plan']} {total_reading_days} {t['days']}")

        # Generate plan with actual dates
        day_index = 0
        pages_read = 0

        for week in range(1, weeks + 1):
            week_goal = (week / weeks) * book_pages
            st.markdown(f"#### 📅 {t['week']} {week}/{weeks} — {t['to_page']} {int(week_goal)}")

            for _ in range(days_per_week):
                if day_index < len(reading_dates):
                    date = reading_dates[day_index]
                    custom_weekday = (date.weekday() + 1) % 7

                    # Add pages for this specific day based on intensity
                    pages_for_day = pages_distribution[custom_weekday]
                    pages_read += pages_for_day

                    formatted_date = format_date(date, lang, short_day=True)

                    # Intensity indicator (if different from 100%)
                    intensity_emoji = " ⚡" if intensities[custom_weekday] != 100 else ""

                    st.write(f"{t['day']} {day_index + 1}/{total_reading_days}: {formatted_date} → **{t['to_page']} {math.ceil(pages_read)}{intensity_emoji}**")
                    day_index += 1

            st.write("")


if __name__ == "__main__":
    main()