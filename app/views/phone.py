import requests
from flask import request, jsonify, current_app


def post_aggregate():
    phones = request.get_json()
    if phones:
        prefixes = get_prefixes()
        result_set = {}
        for p in phones:
            if p.startswith('+'):
                sufix = p.replace('+', '', 1)
            elif p.startswith('00'):
                sufix = p.replace('00', '', 1)
            for valid_prefix in prefixes:
                if sufix.startswith(valid_prefix):
                    sector = get_sector(p)
                    if valid_prefix not in result_set:
                        result_set[valid_prefix] = []
                    result_set[valid_prefix].append(sector['sector'])
                continue
        return format_result(result_set), 200
    else:
        return jsonify({'message': 'Empty post content', 'data': {}}), 500


def get_sector(phone_number):
    if phone_number:
        url = current_app.config['TALKDESK_CHALLENGE_URI'] + phone_number
        try:
            response = requests.get(url=url, params={})
            return response.json()
        except:
            return jsonify({'message': 'TalkDesk API Error', 'data': {}}), 500
    else:
        return jsonify({'message': 'Empty phone number', 'data': {}}), 500


def get_prefixes():
    file_path = current_app.config['PREFIX_FILEPATH']
    with open(file_path) as f:
        prefixes = f.read().splitlines()
        return prefixes


def format_result(result_set):
    formatted_dict = '{'
    for phone_dict in result_set:
        sector_count = 0
        if phone_dict not in formatted_dict:
            if len(formatted_dict) > 1:
                formatted_dict += ','
            formatted_dict += '"' + phone_dict + '":'
        for sector in result_set[phone_dict]:
            sector_count += 1
            if sector not in formatted_dict:
                if sector_count <= 1:
                    formatted_dict += '{'
                formatted_dict += '"' + sector + '":' + str(result_set[phone_dict].count(sector))
                if sector_count < len(result_set[phone_dict]) - 1:
                    formatted_dict += ','
        formatted_dict += '}'
    formatted_dict += '}'
    return formatted_dict
