from datetime import date, timedelta

from ohfandugfmanager.models import OhfAndUgfDetails
from threesaillconnections.models import ThreesaIllDoneConnectionsDetails
from threesaillthroughvendors.models import TTVIllDoneConnectionsDetails
from vendorsillthroughthreesa.models import VTTIllDoneConnectionsDetails


def run_daily_tasks_at4():
    threesa_ill_obj_all = ThreesaIllDoneConnectionsDetails.objects.all()
    for threesa_ill_obj in threesa_ill_obj_all:
        if threesa_ill_obj.billing_code:
            if date.today() >= threesa_ill_obj.billing_code.conn_end_date:
                threesa_ill_obj.active_status = False
                threesa_ill_obj.save()

    ttv_ill_obj_all = TTVIllDoneConnectionsDetails.objects.all()
    for ttv_ill_obj in ttv_ill_obj_all:
        if ttv_ill_obj.billing_code:
            if date.today() >= ttv_ill_obj.billing_code.conn_end_date:
                ttv_ill_obj.active_status = False
                ttv_ill_obj.save()

    vtt_ill_obj_all = VTTIllDoneConnectionsDetails.objects.all()
    for vtt_ill_obj in vtt_ill_obj_all:
        if vtt_ill_obj.billing_code:
            if date.today() >= vtt_ill_obj.billing_code.conn_end_date:
                vtt_ill_obj.active_status = False
                vtt_ill_obj.save()

    OhfAndUgf_obj_all = OhfAndUgfDetails.objects.all()
    for OhfAndUgf_obj in OhfAndUgf_obj_all:
        if OhfAndUgf_obj.link_billing_code:
            if date.today() >= OhfAndUgf_obj.link_billing_code.link_end_date:
                OhfAndUgf_obj.link_status = False
                OhfAndUgf_obj.save()

    print('all done')
