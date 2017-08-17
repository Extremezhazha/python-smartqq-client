import io
from .GetBarcodeStepHandler import GetBarcodeStepHandler
from .GetPsessionidHandler import GetPsessionidHandler
from .GetPtwebqqHandler import GetPtwebqqHandler
from .GetVfwebqqHandler import GetVfwebqqHandler
from .LoginPipeline import LoginPipeline
from .WaitForAuthHandler import WaitForAuthHandler
from .LoginFinalizeHandler import LoginFinalizeHandler
from .LoginSetupHandler import LoginSetupHandler
from .BarcodeExpiredException import BarcodeExpiredException
from .Logger import logger


class SmartqqLoginPipeline(LoginPipeline):
    @staticmethod
    def default_exception_handler(ex):
        if ex.__class__ == BarcodeExpiredException:
            logger.error("Barcode expired, please try again.")
            return True
        logger.error(ex)
        return False

    @staticmethod
    def barcode_store(barcode: io.BytesIO):
        with open("barcode.png", "wb") as barcode_file:
            import shutil
            shutil.copyfileobj(barcode, barcode_file)
            logger.info("Please scan the barcode png to login")
            barcode.seek(0)

    def __init__(self, session, barcode_handler=None, exception_handler=None):
        if exception_handler is None:
            exception_handler = SmartqqLoginPipeline.default_exception_handler
        super().__init__(session, exception_handler)
        self.add_step(LoginSetupHandler(session))
        self.add_step(GetBarcodeStepHandler(session))
        self.add_step(WaitForAuthHandler(
            session,
            barcode_handler=barcode_handler if barcode_handler is not None else SmartqqLoginPipeline.barcode_store)
        )
        self.add_step(GetPtwebqqHandler(session))
        self.add_step(GetVfwebqqHandler(session))
        self.add_step(GetPsessionidHandler(session))
        self.add_step(LoginFinalizeHandler(session))
