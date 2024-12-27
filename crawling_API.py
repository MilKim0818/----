import requests
from config import API_KEY
from datetime import datetime

apikey = API_KEY

def get_data_today():
    
    url = f'http://ecos.bok.or.kr/api/KeyStatisticList/{apikey}/json/kr/1/100'

    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()

        # 디버깅: API 응답 데이터 출력
        print("API 응답 데이터:", result)

        # 데이터 추출
        if "KeyStatisticList" in result and "row" in result["KeyStatisticList"]:
            return {
                "x": [item.get("KEYSTAT_NAME", "Unknown") for item in result["KeyStatisticList"]["row"]],
                "y": [float(item.get("DATA_VALUE", 0)) for item in result["KeyStatisticList"]["row"]],
                "date": [item.get("CYCLE", "Unknown") for item in result["KeyStatisticList"]["row"]]
            }
        else:
            print("예상된 데이터 구조가 아님")
            return {"x": [], "y": [], "date": []}
    except requests.exceptions.RequestException as e:
        print(f"API 요청 에러: {e}")
        return {"x": [], "y": []}


def get_data(query_item, start_date, end_date):
    apikey = API_KEY
    base_url = "http://ecos.bok.or.kr/api/StatisticSearch"

    # Define a dictionary to map query_item to specific codes
    query_stat_codes = {
        "원달러환율": "731Y001",
        "시장금리": "817Y002"
    }

    query_item_codes = {
        "원달러환율": ["0000001"],
        "시장금리": ["010101000", "010210000", "010502000"]
    }

    # Get the corresponding code for the query_item
    stat_code = query_stat_codes.get(query_item)
    item_codes = query_item_codes.get(query_item)

#    if not item_code:
#        return {"error": f"Invalid query item: {query_item}"}

    # Convert date format from YYYY-MM-DD to YYYYMMDD
    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')

    try:
        responses = []
 
        for item_code in item_codes:
            url = f"{base_url}/{apikey}/json/kr/1/10000/{stat_code}/D/{start_date}/{end_date}/{item_code}"
            response = requests.get(url)
            if response.status_code == 200:
                responses.append(response.json())  # 응답 데이터를 리스트에 추가

        # 여러 응답 데이터를 하나로 합치거나 처리
        combined_data = []
        for response in responses:
            combined_data.extend(response["StatisticSearch"]['row'])  # 데이터 병합

        # Debugging: Print API response
        print("API 응답 데이터:", combined_data)

        # Extract data
        return {
                "x": [item.get("ITEM_NAME1") for item in combined_data],
                "y": [float(item.get("DATA_VALUE")) for item in combined_data],
                "date": [item.get("TIME") for item in combined_data]
            }

    except requests.exceptions.RequestException as e:
        print(f"API 요청 에러: {e}")
        return {"x": [], "y": [], "error": str(e)}