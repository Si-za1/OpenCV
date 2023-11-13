import os
import sys

import pandas as pd
from pathlib import Path
from datetime import date
from loguru import logger
from typing import Union, List
from pydantic import BaseModel, field_validator, ValidationError
from PIL import Image, ImageDraw, ImageOps, ImageFont


class Person(BaseModel):
    name: str
    DOB: date
    image_path: Union[str, Path]

    @field_validator('DOB')
    def validate_dob(cls, value):
        today = date.today()
        if value.month != today.month or value.day != today.day:
            logger.error(
                f"DOB must have the same day and month as today. You have provided {value} which doesn't match "
                f"today's date")
            sys.exit()
        return value

    @field_validator('image_path')
    def convert_to_path(cls, value: Union[str, Path]) -> Path:
        if isinstance(value, str):
            return Path(value)
        return value


class BirthdayDataSchema(BaseModel):
    people: List[Person]


class PostCreation:
    def __init__(self,
                 template_source: Union[str, Path] = 'assets/template.png',
                 font_file: Union[str, Path] = "assets/DMSans-default.ttf",
                 output_folder: Union[str, Path] = "output"):
        self.template_source = template_source
        self.font_file = font_file
        os.makedirs(output_folder, exist_ok=True)
        self.output_folder = output_folder

    @staticmethod
    def __load_image(image_path):
        return Image.open(image_path)

    @staticmethod
    def __circular_mask(size):
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        return mask

    def create_post(self, data: Union[list, pd.DataFrame], mask_size: int = 150, max_images_per_template: int = 5,
                    gap_size: int = 50):

        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')

        try:
            valid_data: BirthdayDataSchema = BirthdayDataSchema(people=data)
        except ValidationError as e:
            raise ValueError(f"Invalid input data: {e}")
        except Exception as e:
            raise e
        else:
            output_templates: list = []
            logger.success("Successfully validated the given data")
            all_people = valid_data.people
            templates = [all_people[i:i + max_images_per_template] for i in
                         range(0, len(all_people), max_images_per_template)]

            for template_index, persons in enumerate(templates):
                template = Image.open(self.template_source)
                template = template.convert('RGB')
                template_size = template.size

                total_width: float = min(len(persons), max_images_per_template) * (mask_size + gap_size) - gap_size
                total_height: float = ((len(persons) - 1) // max_images_per_template + 1) * (
                        mask_size + gap_size) - gap_size

                start_x: float = (template_size[0] - total_width) // 2
                start_y: float = ((template_size[1] - total_height) // 2) + 100

                for index, person_info in enumerate(persons):
                    name = person_info.name
                    image_path = person_info.image_path

                    row: int = index // max_images_per_template
                    col: int = index % max_images_per_template

                    x_coord: int = int(start_x + col * (mask_size + gap_size))
                    y_coord: int = int(start_y + row * (mask_size + gap_size))

                    name_position: tuple = (x_coord + mask_size // 2, y_coord + mask_size + gap_size // 2)

                    img: Image = self.__load_image(image_path=image_path)
                    img.thumbnail((mask_size, mask_size))

                    mask: Image = self.__circular_mask(mask_size)

                    img: ImageOps = ImageOps.fit(img, mask.size, method=1, bleed=0.0, centering=(0.5, 0.5))

                    template.paste(img, (x_coord, y_coord), mask)

                    draw: ImageDraw = ImageDraw.Draw(template)
                    font_size: int = int(mask_size / 10)
                    font: ImageFont = ImageFont.truetype(self.font_file, size=font_size)
                    text_width, text_height = draw.textsize(name, font=font)
                    name_position = (name_position[0] - text_width / 2, name_position[1])
                    draw.text(name_position, name, fill=(0, 0, 0), font=font)

                output_template_path: str = os.path.join(self.output_folder, f'Post{template_index+1}.jpg')
                output_templates.append(output_template_path)
                template.save(output_template_path)
        return output_templates
