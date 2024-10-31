import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json
import requests
import statsmodels.api as sm
from pmdarima import auto_arima
import numpy as np

st.set_page_config(page_title="재고 대시보드", layout="wide", initial_sidebar_state="auto")


# 변동량 계산 함수
def calculate_change(current_value, previous_value):
    return current_value - previous_value


def find_best_arima_params(series):
    model = auto_arima(series, seasonal=False, trace=False, error_action='ignore', suppress_warnings=True)
    return model.order


def generate_forecast(series, order):
    model = sm.tsa.ARIMA(series, order=order)
    model_fit = model.fit()
    forecast_result = model_fit.forecast(steps=1)
    # forecast_result를 직접 검사하여 첫 번째 값만 반환하도록 함
    forecast = forecast_result[0] if isinstance(forecast_result, (list, np.ndarray)) else forecast_result
    return forecast


# 온도 습도 변화
def temperature_humidity_changes():
    url = 'http://backend:8000/monitoring-data'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청이 성공했는지 확인
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    st.sidebar.header("날짜 선택")
    selected_date = st.sidebar.date_input("날짜를 선택하세요", value=df['timestamp'].min().date())

    filtered_data = df[df['timestamp'].dt.date == selected_date]

    chart_option = st.sidebar.radio(
        "선택하세요:",
        ('Temperature', 'Humidity', 'Both')
    )

    st.title("Dashboard")
    st.caption(f"{selected_date.strftime('%Y년 %m월 %d일')} 기준")

    st.write('<hr style="margin: 10px 0;">', unsafe_allow_html=True)
    col1, = st.columns([1])

    # 온도 선택시
    if chart_option == 'Temperature':
        with col1:
            st.subheader("Temperature Change")
            temperature_chart = alt.Chart(filtered_data).mark_line(color='red').encode(
                x='timestamp:T',
                y=alt.Y('temperature:Q', scale=alt.Scale(
                    domain=[filtered_data['temperature'].min() - 1, filtered_data['temperature'].max() + 1]),
                        axis=alt.Axis(title='Temperature (°C)')),
                tooltip=['timestamp:T', 'temperature:Q']
            ).properties(
                width='container',
                height=300
            )
            st.altair_chart(temperature_chart, use_container_width=True)

    # 습도 선택시
    elif chart_option == 'Humidity':
        with col1:
            st.subheader("Humidity Change")
            humidity_chart = alt.Chart(filtered_data).mark_line(color='blue').encode(
                x='timestamp:T',
                y=alt.Y('humidity:Q', scale=alt.Scale(
                    domain=[filtered_data['humidity'].min() - 1, filtered_data['humidity'].max() + 1]),
                        axis=alt.Axis(title='Humidity (%)')),
                tooltip=['timestamp:T', 'humidity:Q']
            ).properties(
                width='container',
                height=300
            )
            st.altair_chart(humidity_chart, use_container_width=True)

    # both선택시
    else:
        with col1:
            st.subheader("Temperature and Humidity Change")
            temperature_chart = alt.Chart(filtered_data).mark_line(color='red').encode(
                x='timestamp:T',
                y=alt.Y('temperature:Q', scale=alt.Scale(
                    domain=[filtered_data['temperature'].min() - 1, filtered_data['temperature'].max() + 1]),
                        axis=alt.Axis(title='Temperature (°C)')),
                tooltip=['timestamp:T', 'temperature:Q']
            ).properties(
                width='container',
                height=300
            )

            humidity_chart = alt.Chart(filtered_data).mark_line(color='blue').encode(
                x='timestamp:T',
                y=alt.Y('humidity:Q', scale=alt.Scale(
                    domain=[filtered_data['humidity'].min() - 1, filtered_data['humidity'].max() + 1]),
                        axis=alt.Axis(title='Humidity (%)')),
                tooltip=['timestamp:T', 'humidity:Q']
            ).properties(
                width='container',
                height=300
            )

            combined_chart = alt.layer(temperature_chart, humidity_chart).resolve_scale(
                y='independent'
            ).properties(
                width='container',
                height=300
            )
            st.altair_chart(combined_chart, use_container_width=True)


# 일간 변화를 시각화
def daily_stock_changes():
    url = 'http://backend:8000/transactions/history'
    data_list = []

    try:
        product_id = ['/1', '/2', '/3']
        for pid in product_id:
            response = requests.get(url + pid)
            response.raise_for_status()  # 요청이 성공했는지 확인
            data = response.json()
            data_list.extend(data)
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return

    # JSON 데이터를 DataFrame으로 변환
    data = pd.json_normalize(data_list)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.rename(columns={'product_name': 'quality'}, inplace=True)

    # 데이터 전처리
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['date'] = data['timestamp'].dt.date

    # 날짜 선택
    st.sidebar.header("날짜 선택")
    selected_date = st.sidebar.date_input("날짜를 선택하세요", value=data['timestamp'].min().date())

    # 선택한 날짜의 재고 데이터
    selected_date_data = data[data['date'] == selected_date]

    lastest_date=selected_date + timedelta(days=1)
    # 선택한 날짜의 각 품질별 마지막 재고 값 추출 (선택한 날짜 포함)
    latest_stock_data = data[data['timestamp'] <= pd.to_datetime(lastest_date)].sort_values('timestamp').drop_duplicates('quality', keep='last')

    # 전날 데이터 추출 (선택한 날짜 제외)
    previous_stock_data = data[data['timestamp'] <= pd.to_datetime(selected_date)].sort_values('timestamp').drop_duplicates('quality', keep='last')

    # 현재 재고와 전날 재고 병합 및 비교
    stock_summary = pd.merge(
        latest_stock_data[['quality', 'current_stock']],
        previous_stock_data[['quality', 'current_stock']],
        on='quality',
        how='outer',
        suffixes=('_current', '_previous')
    ).fillna(0)

    stock_summary['change'] = stock_summary.apply(
        lambda row: calculate_change(row['current_stock_current'], row['current_stock_previous']), axis=1
    )

    st.title("Dashboard")
    st.caption(f"{selected_date.strftime('%Y년 %m월 %d일')} 기준")

    col1, col2, col3 = st.columns(3)

    # 특상, 상, 중 품질에 해당하는 데이터 추출 및 표시
    special_data = stock_summary[stock_summary['quality'] == '사과 - 특상']
    good_data = stock_summary[stock_summary['quality'] == '사과 - 상']
    normal_data = stock_summary[stock_summary['quality'] == '사과 - 중']

    # 데이터가 비어있으면 0으로 비어있지 않으면 변화량 계산
    if not special_data.empty:
        col1.metric("사과 - 특상", f'{special_data["current_stock_current"].values[0]}',
                    f'{special_data["change"].values[0]}')
    else:
        col1.metric("사과 - 특상", "0", "0")

    if not good_data.empty:
        col2.metric("사과 - 상", f'{good_data["current_stock_current"].values[0]}',
                    f'{good_data["change"].values[0]}')
    else:
        col2.metric("사과 - 상", "0", "0")

    if not normal_data.empty:
        col3.metric("사과 - 중", f'{normal_data["current_stock_current"].values[0]}',
                    f'{normal_data["change"].values[0]}')
    else:
        col3.metric("사과 - 중", "0", "0")

    st.write('<hr style="margin: 10px 0;">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        # 선택한 날짜의 시간별 재고 변화 시각화
        st.subheader("Stock Change")
        line_chart = alt.Chart(selected_date_data).mark_line().encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('current_stock:Q', title='Stock Count'),
            color='quality:N',
            tooltip=['timestamp:T', 'current_stock:Q', 'quality:N']
        ).properties(
            height=300,
            width=500
        ).interactive()
        st.altair_chart(line_chart, use_container_width=True)

    # 품질별 재고가 가장 많은 시간 구하기
    peak_times = selected_date_data.loc[selected_date_data.groupby('quality')['current_stock'].idxmax()]

    # 품질별 재고가 가장 많은 시간 시각화
    with col2:
        st.subheader("Peak Stock Time")
        peak_chart = alt.Chart(peak_times).mark_bar().encode(
            x=alt.X('timestamp:T', title='Time', axis=alt.Axis(format='%H:%M:%S', title='시간')),
            y=alt.Y('current_stock:Q', title='Stock Count'),
            color='quality:N',
            tooltip=['timestamp:T', 'current_stock:Q', 'quality:N']
        ).properties(
            height=300,
            width=500
        ).interactive()
        st.altair_chart(peak_chart, use_container_width=True)

    # 품질별 현재 재고 비율을 시각화
    st.subheader("Current Stock Ratios by Quality")

    # 선택한 날짜를 포함한 현재 재고 계산
    end_date = pd.to_datetime(selected_date) + timedelta(days=1)
    total_stock_data = data[data['timestamp'] < end_date].sort_values('timestamp').drop_duplicates('quality',
                                                                                                   keep='last')
    total_stock_data = total_stock_data.groupby('quality', as_index=False)['current_stock'].sum()

    pie_chart = alt.Chart(total_stock_data).mark_arc().encode(
        theta=alt.Theta(field="current_stock", type="quantitative"),
        color=alt.Color(field="quality", type="nominal"),
        tooltip=['quality', 'current_stock']
    ).properties(
        height=300
    )
    st.altair_chart(pie_chart, use_container_width=True)


# 기간별 변화를 시각화
def periodic_stock_changes():
    # 데이터 수집은 수정 필요
    url = 'http://backend:8000/transactions/history'
    data = []

    try:
        product_id = ['/1', '/2', '/3']
        for pid in product_id:
            response = requests.get(url + pid)
            response.raise_for_status()  # 요청이 성공했는지 확인
            tmp = response.json()
            data.append(pd.DataFrame(tmp))
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return

    qualities = ['특상', '상', '중']
    for i, df in enumerate(data):
        df['quality'] = qualities[i]

    combined_data = pd.concat(data, ignore_index=True)
    combined_data['date'] = pd.to_datetime(combined_data['timestamp'])

    # 날짜와 품질별로 평균을 계산
    combined_data = combined_data.groupby(['date', 'quality', 'type'], as_index=False)['current_stock'].mean()

    # 입고와 출고를 구분하여 데이터 처리
    store_data = combined_data[combined_data['type'] == 'store'].pivot(index='date', columns='quality',
                                                                       values='current_stock').reset_index().fillna(0)
    release_data = combined_data[combined_data['type'] == 'release'].pivot(index='date', columns='quality',
                                                                           values='current_stock').reset_index().fillna(
        0)

    # 날짜 선택
    st.sidebar.header("날짜 범위 선택")
    start_date = pd.to_datetime(st.sidebar.date_input("시작 날짜", value=store_data['date'].min()))
    end_date = pd.to_datetime(st.sidebar.date_input("종료 날짜", value=store_data['date'].max()))

    # 선택한 날짜 범위에 따라 데이터 필터링
    filtered_store_data = store_data[(store_data['date'] >= start_date) & (store_data['date'] <= end_date)]
    filtered_release_data = release_data[(release_data['date'] >= start_date) & (release_data['date'] <= end_date)]

    # 여기서 부터 시각화 시작
    st.title("Dashboard")
    st.write('<hr style="margin: 10px 0;">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        # 선택한 날짜 범위에 따른 품질별 사과 갯수 변화 시각화
        st.subheader("Stock Change")
        filtered_data_melt = filtered_store_data.melt(id_vars='date', value_vars=['특상', '상', '중'], var_name='quality',
                                                      value_name='quantity')
        line_chart = alt.Chart(filtered_data_melt).mark_line().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color='quality:N',
            tooltip=['date:T', 'quantity:Q', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col1.altair_chart(line_chart, use_container_width=True)

    # 품질별 재고 가장 많은날 구하기
    peak_days = []
    for quality in ['특상', '상', '중']:
        peak_day = filtered_store_data.loc[filtered_store_data[quality].idxmax(), ['date', quality]]
        peak_days.append({'quality': quality, 'date': peak_day['date'], 'quantity': peak_day[quality]})

    peak_data = pd.DataFrame(peak_days)

    # 품질별 재고 가장 많은 날을 막대 차트로 시각화
    with col2:
        st.subheader("Peak Stock Day")
        peak_chart = alt.Chart(peak_data).mark_bar().encode(
            x=alt.X('date:T', title='날짜', timeUnit='yearmonthdate'),
            y=alt.Y('quantity:Q', title='수량'),
            color='quality:N',
            tooltip=['date:T', 'quantity:Q', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col2.altair_chart(peak_chart, use_container_width=True)

    # 입고와 출고 시각화
    store_data_melt = filtered_store_data.melt(id_vars='date', value_vars=['특상', '상', '중'], var_name='quality',
                                               value_name='quantity')
    store_data_melt['type'] = '입고'
    release_data_melt = filtered_release_data.melt(id_vars='date', value_vars=['특상', '상', '중'], var_name='quality',
                                                   value_name='quantity')
    release_data_melt['type'] = '출고'

    col1, col2, col3 = st.columns(3)

    with col1:
        # 입고 시각화 - 특상
        st.subheader("Stock Movement - 특상")
        movement_chart = alt.Chart(store_data_melt[store_data_melt['quality'] == '특상']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['입고'], range=['#1f77b4'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col1.altair_chart(movement_chart, use_container_width=True)

    with col2:
        # 입고 시각화 - 상
        st.subheader("Stock Movement - 상")
        movement_chart = alt.Chart(store_data_melt[store_data_melt['quality'] == '상']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['입고'], range=['#1f77b4'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col2.altair_chart(movement_chart, use_container_width=True)

    with col3:
        # 입고 시각화 - 중
        st.subheader("Stock Movement - 중")
        movement_chart = alt.Chart(store_data_melt[store_data_melt['quality'] == '중']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['입고'], range=['#1f77b4'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col3.altair_chart(movement_chart, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # 출고 시각화 - 특상
        st.subheader("Stock Movement - 특상")
        movement_chart = alt.Chart(release_data_melt[release_data_melt['quality'] == '특상']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['출고'], range=['#ff7f0e'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col1.altair_chart(movement_chart, use_container_width=True)

    with col2:
        # 출고 시각화 - 상
        st.subheader("Stock Movement - 상")
        movement_chart = alt.Chart(release_data_melt[release_data_melt['quality'] == '상']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['출고'], range=['#ff7f0e'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col2.altair_chart(movement_chart, use_container_width=True)

    with col3:
        # 출고 시각화 - 중
        st.subheader("Stock Movement - 중")
        movement_chart = alt.Chart(release_data_melt[release_data_melt['quality'] == '중']).mark_bar().encode(
            x=alt.X('date:T', title='날짜'),
            y=alt.Y('quantity:Q', title='수량'),
            color=alt.Color('type:N', scale=alt.Scale(domain=['출고'], range=['#ff7f0e'])),
            tooltip=['date:T', 'quantity:Q', 'type:N', 'quality:N']
        ).properties(
            height=300
        ).interactive()
        col3.altair_chart(movement_chart, use_container_width=True)

    # 선택한 날짜 범위에 따라 데이터 필터링
    filtered_store_data = store_data[(store_data['date'] >= start_date) & (store_data['date'] <= end_date)]

    if st.sidebar.button('사과 수량 예측'):
        forecast_results = {}
        for quality in filtered_store_data.columns[1:]:  # 첫 번째 열은 'date'임
            quality_data = filtered_store_data[quality]
            if not quality_data.empty:
                order = find_best_arima_params(quality_data)
                forecast = generate_forecast(quality_data, order)
                forecast_results[quality] = forecast

        # 예측 결과를 DataFrame으로 변환
        forecast_df = pd.DataFrame({
            "Quality": list(forecast_results.keys()),
            "Forecast": [int(f) for f in forecast_results.values()]
        })

        # Altair를 사용하여 바 차트 생성
        forecast_chart = alt.Chart(forecast_df).mark_bar().encode(
            y='Quality:N',  # y축에 품질 배치 (수평 바)
            x='Forecast:Q',  # x축에 예측 수량 배치
            color='Quality:N',  # 색상을 품질별로 다르게 설정
            tooltip=['Quality', 'Forecast']  # 툴팁에 표시할 내용
        ).properties(
            width=600,  # 차트의 너비
            height=300  # 차트의 높이
        )

        st.subheader("다음 날 예상 재고")
        st.altair_chart(forecast_chart, use_container_width=True)


def main():
    # 대시보드 모드 선택
    st.sidebar.header("대시보드 선택")
    dashboard_mode = st.sidebar.selectbox("온습도 or 재고", ["Stock Change", "Temperature and Humidity Change"])
    try:
        if dashboard_mode == 'Stock Change':
            st.sidebar.header("재고 변화")
            mode = st.sidebar.selectbox("일별 or 기간별", ["Daily Stock Changes", "Periodic Stock Changes"])

            if mode == "Daily Stock Changes":
                daily_stock_changes()
            elif mode == "Periodic Stock Changes":
                periodic_stock_changes()
        else:
            temperature_humidity_changes()
    except Exception as e:
        st.error(f"대시보드 생성 중 오류가 발생했습니다. 데이터베이스 연동에 실패하였거나 불러올 데이터가 없습니다.")
        st.error(e)
        import traceback
        st.error(traceback.format_exc())


if __name__ == "__main__":
    main()