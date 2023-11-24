from aiogram import F, Router, types, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import commands
import menu
import text
import utils
from states import Gen

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await menu.build_kb(msg)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=menu.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=menu.menu)


@router.callback_query(F.data == commands.generate)
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_gen)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=menu.exit_kb)


@router.message(Gen.img_gen)
@flags.chat_action("upload_photo")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await utils.get_image(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=menu.iexit_kb)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_red)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=menu.exit_kb)


@router.message(Gen.img_red)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=menu.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0])

