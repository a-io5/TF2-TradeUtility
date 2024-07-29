
# Created by Mark Dearman (a-iO5)

from tftu_settings import KEY_VALUE, REC_VALUE, SCR_VALUE

# This could actually be useful, or not. Idk. I just like the calculation ;D

def ref_calculator(total_ref):
    key_value = KEY_VALUE
    rec_value = REC_VALUE
    scr_value = SCR_VALUE
    
    keys = total_ref // key_value
    remaining_ref = total_ref % key_value
    
    recs = remaining_ref // rec_value
    remaining_ref %= rec_value
    
    scrs = remaining_ref // scr_value
    remaining_ref %= scr_value
    
    result = []
    if keys > 0:
        result.append(f"{int(keys)} keys")
    if recs > 0:
        result.append(f"{int(recs)} rec")
    if scrs > 0:
        result.append(f"{int(scrs)} scr")
    if remaining_ref > 0:
        result.append(f"{remaining_ref:.2f} ref")
    
    return ", ".join(result)