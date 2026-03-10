from telegram import Update
from telegram.ext import ContextTypes
from pdf.pdf_manager import approve_pdf, reject_pdf
from config import PDF_STORAGE_CHANNEL


async def handle_pdf_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    action = data[0]
    file_id = data[1]

    if action == "approve_pdf":

        approve_pdf(file_id)

        await context.bot.send_document(
            chat_id=PDF_STORAGE_CHANNEL,
            document=file_id,
            caption="Approved PDF"
        )

        await query.edit_message_caption("PDF Approved.")

    elif action == "reject_pdf":

        reject_pdf(file_id)

        await query.edit_message_caption("PDF Rejected.")
