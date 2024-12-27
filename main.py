from flask import Flask, render_template, request, jsonify
from crawling_API import get_data, get_data_today
from crawl_news import get_news_list
from crawl_weather import get_weather_info

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# Custom filter to use zip in Jinja2 templates
@app.template_filter('zip')
def zip_filter(*args):
    return zip(*args)


@app.route('/')
def home():
    # 홈 페이지 렌더링
    # 렌더링에 사용할 데이터
    response_data = get_data_today()
    additional_data = {
        "value1": response_data['y'][9], # 예금은행 대출금리
        "value2": response_data['y'][13], # 가계신용연체율
        "value3": response_data['y'][22], # 코스피지수
        "value4": response_data['y'][23] # 코스닥지수
    }

    additional_data_2 = {
        "value1": response_data['date'][9], # 예금은행 대출금리
        "value2": response_data['date'][13], # 가계신용연체율
        "value3": response_data['date'][22], # 코스피지수
        "value4": response_data['date'][23] # 코스닥지수
    }    

    # 뉴스 크롤링 (원달러환율, 코스피지수)
    company1_stock = {'title': "원달러환율"}
    company1_news_list = get_news_list("원달러환율")

    company2_stock = {'title': "코스피지수"}
    company2_news_list = get_news_list("코스피지수")

    # 날씨 크롤링
    weather_info = get_weather_info()

    return render_template('index.html', 
                           additional_data=additional_data, 
                           additional_data_2=additional_data_2,
                           company1_stock=company1_stock,
                           company1_news_list=company1_news_list,
                           company2_stock=company2_stock,
                           company2_news_list=company2_news_list,
                           weather_info=weather_info)

@app.route('/line')
def get_line_chart_data():
    return jsonify(['data1', 30, 200, 100, 400, 150, 250])


@app.route('/pie')
def get_pie_chart_data():
    return jsonify([['A', 30], ['B', 50], ['C', 20]])

@app.route('/daily_charts')
def daily_charts():
    # 데일리 차트 페이지 렌더링
    return render_template('daily_charts.html')


@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    query_item = data.get('queryItem')

    # Fetch data based on query parameters
    query_result = get_data(query_item, start_date, end_date)

    # Reset visualization data before sending new results
    reset_visualization()

    # Return the query result as JSON
    return jsonify(query_result)

def reset_visualization():
    # This function can clear any cached data or reset state as needed
    print("Visualization data reset")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)