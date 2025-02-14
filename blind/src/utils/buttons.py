from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keymakers(list_text, list_postdata, add_basics:bool=False, lote=3):
    """**Function Description:**

The `keymakers` function creates an `InlineKeyboardMarkup` object from two lists: one with the text of the buttons and another with the data that will be sent when they are clicked. It also takes a boolean value indicating whether basic buttons (such as a back button) should be added.

**Parameters:**

* `list_text`: A list with the button text.
* `list_postdata`: A list with the data that will be sent when clicking the buttons.
* `add_basics` (optional): A boolean value indicating whether to add basic buttons. The default value is `False`.

**Return value:**

An `InlineKeyboardMarkup` object with the list of buttons.

**Example:**

```python
list_text = ["Button 1", "Button 2"]
list_postdata = ["data1", "data2"]

markup = keymakers(list_text, list_postdata)
```

The code above will create an `InlineKeyboardMarkup` object with two buttons:

* Button 1: Send the data "data1" as callback data.
* Button 2: Send the data "data2" as callback data."""

    lB = []
    buttons = []
    for text, postdata in zip(list_text, list_postdata):
        if postdata.startswith("WEB"):
            url = "-".join(postdata.split("-")[1:])
            lB.append(InlineKeyboardButton(str(text), url=url))
        else:
            lB.append(InlineKeyboardButton(str(text), callback_data=postdata))

    lB = [lB[i:i+lote] for i in range(0, len(list_text), lote)]
        
    if add_basics:
        lB.append([InlineKeyboardButton(str(text), callback_data=str(postdata)) for text, postdata in zip(["Return"], ["start-0"])])
    buttons = InlineKeyboardMarkup(lB)

    return buttons

if __name__ == "__main__":
    botones = keymakers(["text1"], ["postdata1"], True, 1)
    print (botones)