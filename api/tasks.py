# Put your tasks here
import time

from celery.utils.log import get_task_logger

from api.level_generator import image_generator
from api.level_generator.generator import HotlineGenerator
from api.level_generator.models import LevelConfig
from api.models import Level
from hotline import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def generate_level_preview(level_id, level_config):
    logger.info(f"Generating level and preview"
                f" for level_id={level_id},"
                f" config={str(level_config)}")
    generator = HotlineGenerator()
    level_config = LevelConfig(**level_config)
    rooms = generator.generate(level_config)
    logger.debug(f"Level data for level_id={level_id} generated")

    img = image_generator.make_image(level_config, rooms)
    logger.debug(f"Preview for level_id={level_id} generated")

    level = Level.objects.get(pk=level_id)
    level.add_image(img)
    level.save()
    logger.info(f"Level level_id=f{level_id} saved")
