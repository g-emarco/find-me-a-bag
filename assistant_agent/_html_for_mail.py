import jinja2

html_content2 = """"
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    /* Some basic styling to make the email look nice */
    body { font-family: sans-serif; max-width: 100%; width: auto; }
    img { max-width: 100%; height: auto; }
    @media (min-width: 600px) { /* Adjusts the size for screens wider than 600px */
      img { max-width: 25%; } /* Limits image width to 25% of the container on desktop */
    }
  </style>
</head>
<body>

  <h2>Hi!</h2>

  <p>I was thinking about you and saw this beautiful bag. What do you think?</p>
  <p> it is called {{ bag_name }} </>

  <img src="{{ bag_image }}" alt="bag">
    <br><br>
    <p>{{ bag_description }}</p>

    
  <p>I love the rich color, and it seems like the perfect size for everyday use. It looks so stylish and classic, just like you! 😉</p>

  <p>Let me know if you like it, and we can get it for you!</p>
  <p>Love,<br></p>

</body>
</html>

"""

html_content3 = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: Arial, sans-serif;
      color: #333;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }
    .container {
      max-width: 600px;
      margin: 20px auto;
      padding: 20px;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h2 {
      color: #4CAF50;
      font-size: 24px;
    }
    p {
      line-height: 1.6;
      color: #555;
    }
    .bag-image {
      display: block;
      max-width: 150px;
      height: auto;
      margin: 20px 0;
      border-radius: 8px;
    }
    .signature {
      margin-top: 20px;
    }
  </style>
</head>
<body>

  <div class="container">
    <h2>Hi!</h2>

    <p>I was thinking about you and saw this beautiful bag. What do you think?</p>
    <p>It is called {{ bag_name }}.</p>

    <img src="{{ bag_image }}" alt="bag" class="bag-image">
    <p>{{ bag_description }}</p>

    <p>I love the rich color, and it seems like the perfect size for everyday use. It looks so stylish and classic, just like you! 😉</p>

    <p>Let me know if you like it, and we can get it for you!</p>
    <p class="signature">Love,<br>{{ sender_name }}</p>
  </div>

</body>
</html>
"""


def _populate_bag_email(bag_data):
    """Populates an HTML email template with bag data.

    Args:
        bag_data (dict): A dictionary containing bag information:
            - 'image': URL of the bag image.
            - 'dimensions': Dimensions of the bag.
            - 'price': Price of the bag.
            - 'description': A short description of the bag.

    Returns:
        str: The populated HTML email content.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
       <p>{{ bag_name }}</p>
      <img src="{{ image_url }}" alt="Bag Image">
      <p>{{ bag_description }}</p>
      <p>Price: {{ bag_price }}</p>
    </body>
    </html>
    """
    template = jinja2.Template(html_content3)

    data = {
        "image_url": bag_data.get("image_url", ""),
        "bag_price": bag_data.get("bag_price", "Unknown"),
        "bag_description": bag_data.get("bag_description", "A beautiful bag"),
        "bag_name": bag_data.get("bag_name"),
    }

    return template.render(data)
