

import xlrd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from datastream.models import DataStream
from xlrd import xldate

"""
data = 
[number:2016.0,  # 年  0
number:6.0,   # 月      1
number:3.0,   # 日       2
text:'B-1719',  # 机号   3
text:'AQ1071',  # 航班号  4
text:'KWE',     # 地点   5
empty:'',      # 天气     6
empty:'',      #温度   7 
text:'航后',    #故障时段   8
empty:'',      # 故障时段   9
text:'一般',    #故障类型   10
number:33.0,    # 章   11
number:45.0,    # 节   12
text:'航后检查滑行灯不亮。\n',  # 故障描述    13
text:'因贵阳无料，办理C类LSDD,无“M”项“O”项工作，依MEL33-09.',   # 处理措施    14
empty:'',                       # 记录纸号15
text:'MEL33-09',                # MEL/CDL依据文件16
text:'航后参考AMM33-45-01-960-801更换滑行灯灯泡，检查测试正常，完成MCC20160604001指令单，撤保留单DD20160603001.',  # 后续处理措施17
text:'行灯灯泡\n垫圈',         # 拆换件名称18
text:'4551\n51-0308-1',      # 拆下件号19
text:'N/A',                  # 拆下序号20
text:'4551\n51-0308-1',      # 装上件号21
text:'N/A',                  # 装上序号22
text:'2016.6.4',             # 装机时间23
text:'N/A',                  # 延误性质24
text:'N/A',                  # 延误原因25
text:'N/A',                  # 延误说明26
text:'N/A',                  # 延误时间27
text:'N/A',                  #  故障后果28
text:'N/A',                  # SDR29
text:'N/A',                  # 更换飞机30
text:'N/A',                  # 非计划停场天数31
text:'2017.2.15',            # 录入时间32
text:'姚景乐',                # 录入人员33
text:'梁浩荣']                # 审核人员34
[['id', 'ID'],
 ['the_year', '年'],
 ['the_month', '月'],
 ['the_day', '日'],
 ['aircraft_code', '机号'],
 ['flight_type', '航班号'],
 ['location', '地点'],
 ['weather', '天气'],
 ['temperature', '温度'],
 ['fault_phase', '故障阶段'],
 ['fault_description', '故障描述'],
 ['fault_type', '故障类型'],
 ['chapter', '章'],
 ['knob', '节'],
 ['deal_method', '处理措施'],
 ['record_paper_code', '记录纸号'],
 ['mel_or_cdl_file', 'MEL/CDL依据文件'],
 ['parts_name', '拆换件名称'],
 ['strike_parts_code', '拆下件号'],
 ['strike_parts_num', '拆下序号'],
 ['mount_parts_code', '装上件号'],
 ['mount_parts_num', '装上序号'],
 ['mount_date', '装机时间'],
 ['fault_result', '故障后果'],
 ['delay_reason', '延误原因'],
 ['delay_time', '延误时间'],
 ['has_delayed', '是否延误'],
 ['is_sdr', '是否SDR'],
 ['unexpected_stay_day', '非计划停场天数'],
 ['create_time', '录入时间'],
 ['create_user', '录入人员'],
 ['has_checked', '完成审核?'],
 ['check_user', '审核人员'],
 ['status', '状态']]

"""
from django.utils.dateformat import datetime

DATA_INPUT_FORMAT = [
    '%Y-%m-%d',
    '%Y.%m.%d',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%b %d %Y',
    '%b %d, %Y',
    '%d %b %Y',
    '%d %b, %Y',
    '%B %d %Y',
    '%B %d, %Y',
    '%d %B %Y',
    '%d %B, %Y'
]

cached = {}


class ExportField(object):
    def __init__(self, filed_name, row_index, parse_method=None):
        self.filed_name = filed_name
        self.row_index = row_index
        self.parse_method = parse_method or self.default_parse_method

    def parse_data(self, row):
        value = row[self.row_index].value
        return self.parse_method(value)

    def default_parse_method(self, value):
        return str(value) or "N/A"


def parse_temperature(value):
    try:
        temperature = int(value)
        if temperature > 28:
            return "28度以上"
        elif 10 <= temperature <= 28:
            return "28度"
        else:
            return "10度以下"
    except (TypeError, ValueError):
        return "10-28度"


def parse_fault_phase(value):
    if isinstance(value, float):
        return int(value)
    elif value.strip() == "航前":
        return 1
    else:
        return 10


def parse_fault_type(value):
    data = {
        "一般": 1,
        "突发": 2,
        "重复": 3,
        "疑难": 4,
        "重大": 5
    }
    return data.get(value, 1)


def parse_mount_date(value):
    if isinstance(value, float):
        result = xldate.xldate_as_datetime(value, False)
        cached["datetime"] = result
        return result

    for formatter in DATA_INPUT_FORMAT:
        try:
            result = datetime.datetime.strptime(value, formatter)
            cached["datetime"] = result
            return result
        except (ValueError, TypeError, AttributeError):
            pass
    return cached["datetime"]


def parse_delay_time(value):
    if value and str(value).strip() != "N/A":
        for formatter in DATA_INPUT_FORMAT:
            try:
                result = datetime.datetime.strptime(value , formatter)
                cached["datetime"] = result
                return result
            except (ValueError, TypeError, AttributeError):
                pass
    return "N/A"

def pares_year(value):
    try:
        cached["year"] = int(value)
        return int(value)
    except (ValueError, ):
        return cached["year"]

def parse_month(value):
    try:
        cached["month"] = int(value)
        return int(value)
    except (ValueError, ):
        return cached["month"]

def parse_day(value):
    try:
        cached["day"] = int(value)
        return int(value)
    except (ValueError, ):
        return cached["day"]

def parse_user(user):
    obj, status = User.objects.get_or_create(username=str(user.strip()), defaults={
        "is_staff": True, "password": "9air.com"})
    return obj


def parse_has_checked(value):
    return True

def parse_status(value):
    return 0


class DataStreamExport(object):
    class Meta:
        fields = ['after_deal_method', 'aircraft_code', 'chapter', 'check_user',
                  'create_time', 'create_user', 'deal_method', 'delay_reason',
                  'delay_time', 'fault_description', 'fault_phase',
                  'fault_type', 'flight_type', 'has_checked', 'knob', 'location',
                  'mel_or_cdl_file', 'mount_date', 'mount_parts_code', 'mount_parts_num',
                  'parts_name', 'record_paper_code', 'status', 'strike_parts_code',
                  'strike_parts_num', 'temperature', 'the_day', 'the_month',
                  'the_year', 'weather']

    the_year = ExportField("the_year", 0, pares_year)
    the_month = ExportField("the_month", 1, parse_month)
    the_day = ExportField("the_day", 2, parse_day)
    aircraft_code = ExportField("aircraft_code", 3)
    flight_type = ExportField("flight_type", 4)
    location = ExportField("location", 5)
    weather = ExportField("weather", 6)
    temperature = ExportField("temperature", 7, parse_temperature)
    fault_phase = ExportField("fault_phase", 8, parse_fault_phase)
    fault_type = ExportField("fault_type", 10, parse_fault_type)
    fault_description = ExportField("fault_description", 13)
    chapter = ExportField("chapter", 11)
    knob = ExportField("knob", 12)
    deal_method = ExportField("deal_method", 14)
    record_paper_code = ExportField("record_paper_code", 15)
    mel_or_cdl_file = ExportField("mel_or_cdl_file", 16)
    after_deal_method = ExportField("after_deal_method", 17)
    parts_name = ExportField("parts_name", 18)
    strike_parts_code = ExportField("strike_parts_code", 19)
    strike_parts_num = ExportField("strike_parts_num", 20)
    mount_parts_code = ExportField("mount_parts_code", 21)
    mount_parts_num = ExportField("mount_parts_num", 22)
    mount_date = ExportField("mount_date", 23, parse_mount_date)
    delay_reason = ExportField("delay_reason", 25)
    delay_time = ExportField("delay_time", 27, parse_delay_time)
    create_time = ExportField("create_time", 32, parse_mount_date)
    create_user = ExportField("create_user", 33, parse_user)
    check_user = ExportField("check_user", 34, parse_user)
    #
    has_checked = ExportField("has_checked", 32, parse_has_checked)
    status = ExportField("has_checked", 32, parse_status)

    @classmethod
    def parse_data(cls, row):
        data = {}
        for field_name in cls.Meta.fields:
            field = getattr(cls, field_name)
            data.update({field.filed_name: field.parse_data(row)})
        return data


class Command(BaseCommand):
    help = '导入数据'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        datastream = xlrd.open_workbook(file_path)
        gzlr = datastream.sheet_by_index(0)   # 故障录入
        error_rows = []
        for rx in range(2, gzlr.nrows):
            try:
                row = gzlr.row(rx)
                DataStream.objects.create(**DataStreamExport.parse_data(row))
            except Exception:
                error_rows.append(row)
        print(error_rows)
