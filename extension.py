from datetime import datetime
import logs
from typing import List
log = logs.get_logger(__name__)


def ext_update(newest: list) -> List[str]:
    update = []
    for up in newest:
        date = datetime.strptime(up, '%Y-%m-%d')
        days = (datetime.now() - date).days
        if days > 365:
            update.append('停更')
        elif days > 30 * 6:
            update.append('停更风险')
        elif days > 30 * 3:
            update.append('暂时停更')
        elif days > 30:
            update.append('更新缓慢')
        else:
            update.append('仍在更新')
    return update


def ext_fans_level(fans: list) -> List[str]:
    fans_levels = ('0-100',
                   '100-1000',
                   '1000-1万',
                   '1万-10万',
                   '10万-50万',
                   '50万-100万',
                   '100万-300万',
                   '>300万')
    fans_level = []
    for fan in fans:
        if fan > 300*10000:
            level = 7
        elif fan > 100*10000:
            level = 6
        elif fan > 50*10000:
            level = 5
        elif fan > 10*10000:
            level = 4
        elif fan > 10000:
            level = 3
        elif fan > 1000:
            level =2
        elif fan > 100:
            level = 1
        else:
            level = 0
        fans_level.append(fans_levels[level])
    return fans_level

def ext_single_field(fields:list)->List[str]:
    single_field = [i.split(',')[0] for i in fields]
    return single_field

def ext_big_field(fields:list)->List[str]:
    single_field = ext_single_field(fields)
    big_field = []
    for i in single_field:
        if i in ('电影','纪录片','影视','动画','国创'):
            field_type = '泛影视'
        elif i in ('音乐','舞蹈','游戏','鬼畜','娱乐'):
            field_type = '泛娱乐'
        elif i in ('知识','科技','资讯'):
            field_type = '泛知识'
        elif i in ('生活','美食','动物圈','汽车','时尚','运动'):
            field_type = '泛生活'
        else:
            field_type = '无'
        big_field.append(field_type)
    return big_field
    
