from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class OrderDataUser(StatesGroup):
    time_wait = State()
    brand_wait = State()
    distant_of_car = State()
    day_wait = State()
    action_wait = State()

    product_sp2 = State()

    after_search_sklad = State()
    search_sklad_str = State()
    product_sklad1 = State()
    product_sklad2 = State()

    sklad_keyb_st = State()

    state_photo_get = State()
    prih_uh_st = State()
    prihod_make_st = State()
    uh_make_st = State()

    # РАСС
    adv_ph_c_wait2 = State()

    st_get_mes_to_rassilka = State()

    st_prof_keyb = State()
    st_get_new_fil = State()