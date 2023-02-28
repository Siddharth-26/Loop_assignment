from django.db import connections
import csv
from django.http import FileResponse
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection, connections
import bisect
from django.http import JsonResponse
import pytz
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import asyncio
import time
import aiomysql
from threading import Thread
import io


def last_hour_uptime(lst, status_lst, store_details, last_updated_datetime):
    current_datetime = datetime.datetime.now()
    current_day = current_datetime.weekday()
    one_hour_ago = current_datetime - datetime.timedelta(hours=1)
    one_day_ago = current_datetime-datetime.timedelta(days=1)
    if (last_updated_datetime < one_hour_ago):
        return [0, 1]
    elif (last_updated_datetime >= one_hour_ago and last_updated_datetime < current_datetime):
        current_datetime = last_updated_datetime
    if (current_day in store_details[1]):
        [store_opening, store_closing] = store_details[1][current_day]
        store_opening = datetime.datetime.combine(
            current_datetime.date(), store_opening)
        store_closing = datetime.datetime.combine(
            current_datetime.date(), store_closing)
    else:
        [store_opening, store_closing] = [datetime.datetime.strptime(
            "00:00:00", '%H:%M:%S').time(), datetime.datetime.strptime(
            "00:00:00", '%H:%M:%S').time()]
        store_opening = datetime.datetime.combine(
            one_day_ago.date(), store_opening)
        store_closing = datetime.datetime.combine(
            current_datetime.date(), store_closing)
    useful_list = []
    useful_status_lst = []
    for i in range(len(lst)):
        if (lst[i] >= one_hour_ago and lst[i] <= current_datetime):
            useful_list.append(lst[i])
            useful_status_lst.append(status_lst[i])
    if (store_opening != store_closing):
        if (current_datetime < store_opening or one_hour_ago > store_closing):
            return [0, 0]
        else:
            if (one_hour_ago >= store_opening and current_datetime <= store_closing):
                start_index = bisect.bisect_left(lst, one_hour_ago)
                end_index = bisect.bisect_left(lst, current_datetime)
                start_status = status_lst[start_index-1]
                if (useful_list[0] > one_hour_ago):
                    useful_list = [one_hour_ago]+useful_list
                    useful_status_lst = [start_status]+useful_status_lst
                if (useful_list[-1] < current_datetime):
                    useful_list.append(current_datetime)
                i = 0
                uptime = 0
                downtime = 0
                while (i < len(useful_list)-1):
                    start = useful_list[i]
                    end = useful_list[i+1]
                    if (useful_status_lst[i] == "active"):
                        uptime += round(end-start.total_seconds()/60)
                    else:
                        downtime += round(end-start.total_seconds()/60)
                    i += 1
                return [uptime, downtime]
            elif (one_hour_ago < store_opening and current_datetime < store_closing):
                start_index = bisect.bisect_left(lst, store_opening)
                start_status = status_lst[start_index-1]
                i = 0
                while (i < len(useful_list)):
                    if (useful_list[i] < store_opening):
                        i += 1
                        continue
                    else:
                        break
                useful_list = [store_opening]+useful_list[i:]
                useful_status_lst = ["inactive"]+useful_status_lst[i:]
                i = 0
                uptime = 0
                downtime = 0
                while (i < len(useful_list)-1):
                    start = useful_list[i]
                    end = useful_list[i+1]
                    if (useful_status_lst[i] == "active"):
                        uptime += round(end-start.total_seconds()/60)
                    else:
                        downtime += round(end-start.total_seconds()/60)
                    i += 1
                return [uptime, downtime]
            elif (one_hour_ago > store_opening and current_datetime > store_closing):
                i = 0
                while (i < len(useful_list)):
                    if (useful_list[i] < store_closing):
                        i += 1
                        continue
                    else:
                        break
                useful_list = useful_list[:i]+[store_closing]
                useful_status_lst = useful_status_lst+["inactive"]
                i = 0
                uptime = 0
                downtime = 0
                while (i < len(useful_list)-1):
                    start = useful_list[i]
                    end = useful_list[i+1]
                    if (useful_status_lst[i] == "active"):
                        uptime += round(end-start.total_seconds()/60)
                    else:
                        downtime += round(end-start.total_seconds()/60)
                    i += 1
                return [uptime, downtime]
    else:
        if (one_hour_ago >= store_opening and current_datetime <= store_closing):
            start_index = bisect.bisect_left(lst, one_hour_ago)
            end_index = bisect.bisect_left(lst, current_datetime)
            start_status = status_lst[start_index-1]
            if (useful_list[0] > one_hour_ago):
                useful_list = [one_hour_ago]+useful_list
                useful_status_lst = [start_status]+useful_status_lst
            if (useful_list[-1] < current_datetime):
                useful_list.append(current_datetime)
            i = 0
            uptime = 0
            downtime = 0
            while (i < len(useful_list)-1):
                start = useful_list[i]
                end = useful_list[i+1]
                if (useful_status_lst[i] == "active"):
                    uptime += round(end-start.total_seconds()/60)
                else:
                    downtime += round(end-start.total_seconds()/60)
                i += 1
            return [uptime, downtime]


def calculate_day_uptime(store_opening, store_closing, lst, status_lst, store_details):
    useful_list = []
    useful_status_lst = []
    for i in range(len(lst)):
        if (lst[i] >= store_opening and lst[i] <= store_closing):
            useful_list.append(lst[i])
            useful_status_lst.append(status_lst[i])
    if (store_opening != store_closing):
        start_index = bisect.bisect_left(lst, store_opening)
        start_status = status_lst[start_index]
        if (useful_list[0] > store_opening):
            useful_list = [store_opening]+useful_list
            useful_status_lst = ['closed']+useful_status_lst
        if (useful_list[-1] < store_closing):
            useful_list.append(store_closing)
        i = 0
        uptime = 0
        downtime = 0
        while (i < len(useful_list)-1):
            start = useful_list[i]
            end = useful_list[i+1]
            if (useful_status_lst[i] == "active"):
                uptime += round(((end-start).total_seconds())/3600)
            else:
                downtime += round(((end-start).total_seconds())/3600)
            i += 1
        return [uptime, downtime]

# This functions calculates the last days uptime and downtime. Example : Lets say that today is 25th Feb 2023 then the this function returns the uptime for 24th Feb 2023


def last_day_uptime(day_to_calculate, lst, status_lst, store_details, last_updated_status_datetime):
    current_datetime = day_to_calculate
    current_day = current_datetime.weekday()
    one_day_ago_datetime = current_datetime - datetime.timedelta(days=1)
    uptime = 0
    downtime = 0
    if (current_day in store_details[1]):
        [store_opening, store_closing] = store_details[1][current_day]
        if (store_opening != store_closing):
            store_opening = datetime.datetime.combine(
                one_day_ago_datetime.date(), store_opening)
            store_closing = datetime.datetime.combine(
                one_day_ago_datetime.date(), store_closing)
        else:
            [store_opening, store_closing] = [datetime.datetime.strptime(
                "00:00:00", '%H:%M:%S').time(), datetime.datetime.strptime(
                "00:00:00", '%H:%M:%S').time()]
            store_opening = datetime.datetime.combine(
                one_day_ago_datetime.date(), store_opening)
            store_closing = datetime.datetime.combine(
                current_datetime.date(), store_closing)

    else:
        [store_opening, store_closing] = [datetime.datetime.strptime(
            "00:00:00", '%H:%M:%S').time(), datetime.datetime.strptime(
            "00:00:00", '%H:%M:%S').time()]
        store_opening = datetime.datetime.combine(
            one_day_ago_datetime.date(), store_opening)
        store_closing = datetime.datetime.combine(
            current_datetime.date(), store_closing)
    if (last_updated_status_datetime.date() < day_to_calculate.date()):
        uptime = 0
        downtime = round((store_closing-store_opening).total_seconds()/3600)
        return [uptime, downtime]
    [uptime, downtime] = calculate_day_uptime(store_opening, store_closing,
                                              lst, status_lst, store_details)
    return [uptime, downtime]

# This functions calculates the last weeks uptime and downtime starting from the day before and going back 7 days


def last_week_uptime(lst, status_lst,  store_details, last_updated_datetime):
    current_datetime = datetime.datetime.now()
    uptime = 0
    downtime = 0
    for i in range(1, 7):
        day_to_calculate = current_datetime - datetime.timedelta(days=i)
        [calculated_uptime, calculated_downtime] = last_day_uptime(
            day_to_calculate, lst, status_lst, store_details, last_updated_datetime)
        if (calculated_uptime):
            uptime += calculated_uptime
        if (calculated_downtime):
            downtime += calculated_downtime
    return [uptime, downtime]


@sync_to_async
def create_report():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT store_id from store_status")
            store_details = {}
            for row in cursor.fetchall():
                store_details[row] = None
            for key in store_details:
                cursor.execute(
                    "SELECT store_id, MIN(timezone_str) AS timezone_str FROM store_timezones where store_id=%s", (key, ))
                for row in cursor.fetchall():
                    value = row[1]
                    if (value == None):
                        value = 'America/Chicago'
                    store_details[key] = value
            current_time = datetime.datetime.utcnow()
            for key in store_details:
                current_hour = current_time.hour
                cursor.execute(
                    "SELECT * FROM store_hours where store_id=%s", (key,))
                dic = {}
                arr = list(cursor.fetchall())
                if (len(arr)):
                    for r in cursor.fetchall():
                        day_of_week = r[1]
                        store_opening_time = r[2]
                        store_closing_time = r[3]
                        local_timezone = pytz.timezone(store_details[key])
                        store_opening_time = datetime.datetime.strptime(
                            store_opening_time, '%H:%M:%S').time()
                        store_closing_time = datetime.datetime.strptime(
                            store_closing_time, '%H:%M:%S').time()
                        store_opening_utc_time = local_timezone.localize(
                            store_opening_time).astimezone(pytz.utc)
                        store_closing_utc_time = local_timezone.localize(
                            store_closing_time).astimezone(pytz.utc)
                        dic[day_of_week] = [
                            store_opening_utc_time, store_closing_utc_time]
                else:
                    for i in range(7):
                        day_of_week = i
                        store_opening_time = datetime.datetime.strptime(
                            "00:00:00", '%H:%M:%S').time()
                        store_closing_time = datetime.datetime.strptime(
                            "00:00:00", '%H:%M:%S').time()
                        dic[day_of_week] = [
                            store_opening_time, store_closing_time]
                store_details[key] = [store_details[key], dic]
                cursor.execute(
                    "SELECT *  FROM store_status WHERE store_id = %s AND timestamp_utc BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() order by timestamp_utc desc;", (key,))
                lst = []
                status_lst = []
                activity_array = cursor.fetchall()
                if (len(activity_array)):
                    for r in activity_array:
                        status = r[1]
                        stamp = r[2]
                        lst.append(stamp)
                        status_lst.append(status)
                else:
                    cursor.execute(
                        "SELECT * FROM store_status where store_id=%s order by timestamp_utc desc", (key,))
                    for r in cursor.fetchall():
                        status = r[1]
                        stamp = r[2]
                        lst.append(stamp)
                        status_lst.append(status)
                        break

                proper_lst = []
                for i in range(len(lst)):
                    proper_lst.append([lst[i], status_lst[i]])
                proper_lst.sort(key=lambda x: x[0])
                for i in range(len(lst)):
                    lst[i] = proper_lst[i][0]
                    status_lst[i] = proper_lst[i][1]
                # lst contains the store for the timestamps for the last week in descending order of date and time, storedetails contains a dictionary of stores and their start and endtime in UTC.
                last_hour_result = last_hour_uptime(
                    lst, status_lst,  store_details[key], lst[0])
                if (last_hour_result):
                    [uptime_last_hour, downtime_last_hour] = last_hour_result
                else:
                    [uptime_last_hour, downtime_last_hour] = [None, None]
                last_day_result = last_day_uptime(datetime.datetime.now(),
                                                  lst, status_lst,  store_details[key], lst[0])
                if (last_day_result):
                    [uptime_last_day, downtime_last_day] = last_day_result
                else:
                    [uptime_last_day, downtime_last_day] = [None, None]
                last_week_result = last_week_uptime(
                    lst, status_lst,  store_details[key], lst[0])
                if (last_week_result):
                    [uptime_last_week, downtime_last_week] = last_week_result
                else:
                    [uptime_last_week, downtime_last_week] = [None, None]
                my_list = [key, uptime_last_hour, downtime_last_hour, uptime_last_day,
                           downtime_last_day, uptime_last_week, downtime_last_week]
                filename = 'my_csv_file.csv'
                with open(filename, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(my_list)
                with open(filename, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        print(row)
            cursor.execute(
                "SELECT report_id from report_status order by report_id desc;")
            for r in cursor.fetchall():
                report_id = r[0]
                report_content = r[2]
            content = None
            with open('myfile.csv', 'rb') as f:
                content = f.read()
            content = io.BytesIO(content)
            if (report_id and not report_content and content):
                cursor.execute(
                    "UPDATE report_status SET report_content=%s, report_status=%s WHERE report_id=%s",
                    [content.getvalue(), "Completed", report_id]
                )
            return JsonResponse({"status": 200, "message": "The request was completed successfully."})
    except:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM report_status order by report_id Desc")
            report_id = None
            for row in cursor.fetchall():
                report_id = row[0]
                break
            cursor.execute(
                "DELETE FROM report_status where report_id=%s", (report_id))
            return JsonResponse({"status": 500, "message": "The request was not able completed successfully."})


def run_create_report():
    asyncio.run(create_report())


async def trigger_report(request):
    try:
        pool = await aiomysql.create_pool(
            host='localhost',
            port=3306,
            user='root',
            password='Siddharth@26',
            db='assignment',
            autocommit=True
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO report_status set report_status=%s", ("Running", ))
                await cursor.execute("SELECT * from report_status order by report_id desc")
                arr = await cursor.fetchall()
                report_id = arr[0][0]
                Thread(target=run_create_report).start()
                return JsonResponse({"report_id": report_id})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500, "message": "Something went wrong while calling the API"})


def get_report(request):
    try:
        report_id = request.GET.get("report_id")
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from report_status where report_id=%s", (str(report_id),))
            for r in cursor.fetchall():
                status = r[1]
                content = r[2]
                break
            if (status == "Completed"):
                file_like = io.BytesIO(content)
                response = HttpResponse(
                    file_like, content_type='application/csv')
                response['Content-Disposition'] = f'attachment; filename="{report_id}"'
                return response
            else:
                return JsonResponse({'status': status})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500})


def insert_into_table():
    with connection.cursor() as cursor:
        report_id = 11
        content = None
        with open('my_csv_file.csv', 'rb') as f:
            content = f.read()
        content = io.BytesIO(content)
        if (report_id and content):
            cursor.execute(
                "UPDATE report_status SET report_content=%s, report_status=%s WHERE report_id=%s",
                [content.getvalue(), "Completed", report_id]
            )


insert_into_table()
