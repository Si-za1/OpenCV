import os
import sys

import pandas as pd
from pathlib import Path
from datetime import date
from loguru import logger
from typing import Union, List, Tuple
from pydantic import BaseModel, field_validator, ValidationError
from PIL import Image, ImageDraw, ImageOps, ImageFont


class Person(BaseModel):
    """
    Represents a person with name, date of birth (DOB), and image path.

    Attributes:
        name (str): The name of the person.
        image_path (Union[str, Path]): The path to the image of the person.
    """

    name: str
    image_path: Union[str, Path]

    @field_validator('image_path')
    def convert_to_path(cls, value: Union[str, Path]) -> Path:
        """
        Convert the image path to a Path object if it's a string.

        Args:
            value (Union[str, Path]): The image path.

        Returns:
            Path: The converted image path.
        """
        if isinstance(value, str):
            return Path(value)
        return value


class BirthdayDataSchema(BaseModel):
    """
    Represents the schema for birthday data, including a list of people.

    Attributes:
        people (List[Person]): A list of Person objects.
    """

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
    def __load_image(image_path: Union[str, Path]) -> Image:
        """
        Load an image from the given path.

        Args:
            image_path (Union[str, Path]): The path to the image.

        Returns:
            Image: The loaded image.
        """
        return Image.open(image_path)

    @staticmethod
    def __circular_mask(size: int) -> Image:
        """
        Create a circular mask of the given size.

        Args:
            size (int): The size of the circular mask.

        Returns:
            Image: The circular mask.
        """
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        return mask

    def create_post(self,
                    data: Union[list, pd.DataFrame],
                    mask_size: int = 150,
                    max_images_per_template: int = 5,
                    gap_size: int = 50,
                    circular_border_thickness: int = 3,
                    circular_border_color: Tuple[int, int, int] = (255, 255, 255)) -> list:
        """
        Create birthday celebration posts based on the input data.

        Args:
            data (Union[list, pd.DataFrame]): Input data containing information about people.
            mask_size (int): The size of the circular mask.
            max_images_per_template (int): Maximum number of images per template.
            gap_size (int): Gap size between images.
            circular_border_thickness (int): Thickness of the circular border.
            circular_border_color (Tuple[int, int, int]): Color of the circular border.

        Returns:
            list: List of paths to the generated posts.
        """
        # Check if data is a DataFrame and convert it to a list of dictionaries
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')

        try:
            # Validate input data using a predefined schema
            valid_data: BirthdayDataSchema = BirthdayDataSchema(people=data)
        except ValidationError as e:
            # Log and raise an error if validation fails
            logger.error(f"Invalid input data: {e}")
            raise ValueError
        except Exception as e:
            # Log and raise any other exceptions that occur during validation
            logger.error(f"Exception Occurred: {e}")
            raise e
        else:
            # If validation is successful, proceed with post creation
            output_templates: list = []
            logger.success("Successfully validated the given data")
            all_people = valid_data.people
            templates = [all_people[i:i + max_images_per_template] for i in
                         range(0, len(all_people), max_images_per_template)]

            for template_index, persons in enumerate(templates):
                # Open the template image and convert it to RGB
                template = Image.open(self.template_source)
                template = template.convert('RGB')
                template_size = template.size

                # Calculate total width and height of the template based on the number of persons
                total_width: float = min(len(persons), max_images_per_template) * (mask_size + gap_size) - gap_size
                total_height: float = ((len(persons) - 1) // max_images_per_template + 1) * (
                        mask_size + gap_size) - gap_size

                # Calculate starting coordinates for placing images on the template
                start_x: float = (template_size[0] - total_width) // 2
                start_y: float = ((template_size[1] - total_height) // 2) + 100

                for index, person_info in enumerate(persons):
                    # Extract information about the person
                    name = person_info.name
                    image_path = person_info.image_path

                    # Calculate coordinates for placing the circular mask and text
                    row: int = index // max_images_per_template
                    col: int = index % max_images_per_template
                    x_coord: int = int(start_x + col * (mask_size + gap_size))
                    y_coord: int = int(start_y + row * (mask_size + gap_size))
                    name_position: tuple = (x_coord + mask_size // 2, y_coord + mask_size + gap_size // 2)

                    # Load and resize the person's image, apply circular mask, and paste it onto the template
                    img: Image = self.__load_image(image_path=image_path)
                    img.thumbnail((mask_size, mask_size))
                    mask: Image = self.__circular_mask(mask_size)
                    img: ImageOps = ImageOps.fit(img, mask.size, method=1, bleed=0.0, centering=(0.5, 0.5))
                    template.paste(img, (x_coord, y_coord), mask)

                    # Draw a colored border around the circular mask
                    draw_outline: ImageDraw = ImageDraw.Draw(template)
                    draw_outline.ellipse((x_coord - circular_border_thickness, y_coord - circular_border_thickness,
                                          x_coord + mask_size + circular_border_thickness,
                                          y_coord + mask_size + circular_border_thickness),
                                         outline=circular_border_color, width=circular_border_thickness)

                    # Draw the person's name below the circular mask
                    draw: ImageDraw = ImageDraw.Draw(template)
                    font_size: int = int(mask_size / 10)
                    font: ImageFont = ImageFont.truetype(self.font_file, size=font_size)
                    text_width, text_height = draw.textsize(name, font=font)
                    name_position = (name_position[0] - text_width / 2, name_position[1])
                    draw.text(name_position, name, fill=(0, 0, 0), font=font)

                # Save the generated template and log success
                output_template_path: str = os.path.join(self.output_folder, f'Post{template_index + 1}.jpg')
                output_templates.append(output_template_path)
                template.save(output_template_path)
                logger.success(f"Successfully created {output_template_path}")

        # Return the list of paths to the generated posts
        return output_templates
