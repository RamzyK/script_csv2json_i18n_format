# script_csv2json_i18n_format
This script can generate 3 json files in 3 languages handled (french, english, 
spanish) when taking in parameter the version number of the traduction and a path to 
a CSV file formatted as follow:

|Cle    |French|English|Spanish|
|-------|--------|-------|---------|
|a.b.d.e|toto0   |tutu0  |titi0    |
|b.cc.dd|toto1   |tutu1  |titi1    |
|a.b.d.f|toto2   |tutu2  |titi2    |
|a      |toto3   |toto3  |tutu3    |
|d.f.g  |toto4   |tutu4  |tit4     |


The names in the columns of the first lines is not important. What is important 
though is that there mus be no '\n' characters in the columns 1, 2, 3 because it 
will lead to a crash of the script.

the script applied to the previous CSV file will generate 3 JSON files each looking 
as follow:

carto_static_text_fr.json:
-------------------------
```json
{
  "a": {
    "text": "toto3",
    "accesibilty_description": "",
    "b": {
      "d": {
        "e": {
          "text": "toto0",
          "accesibilty_description": ""
        },
        "f": {
          "text": "toto2",
          "accesibilty_description": ""
        }
      }
    }
  },
  "b": {
    "cc": {
      "dd": {
        "text": "toto1",
        "accesibilty_description": ""
      }
    }
  },
  "d": {
    "f": {
      "g": {
        "text": "toto4",
        "accesibilty_description": ""
      }
    }
  },
  "language": {
    "code": "fr",
    "version": "5"
  }
}
```

carto_static_text_en.json.json:
------------------------------

```json
{
  "a": {
    "text": "toto3",
    "accesibilty_description": "",
    "b": {
      "d": {
        "e": {
          "text": "tutu0",
          "accesibilty_description": ""
        },
        "f": {
          "text": "tutu2",
          "accesibilty_description": ""
        }
      }
    }
  },
  "b": {
    "cc": {
      "dd": {
        "text": "tutu1",
        "accesibilty_description": ""
      }
    }
  },
  "d": {
    "f": {
      "g": {
        "text": "tutu4",
        "accesibilty_description": ""
      }
    }
  },
  "language": {
    "code": "en",
    "version": "5"
  }
}
```
}

carto_static_text_es.json:
-------------------------

```json
{
  "a": {
    "text": "tutu3",
    "accesibilty_description": "",
    "b": {
      "d": {
        "e": {
          "text": "titi0\n",
          "accesibilty_description": ""
        },
        "f": {
          "text": "titi2\n",
          "accesibilty_description": ""
        }
      }
    }
  },
  "b": {
    "cc": {
      "dd": {
        "text": "titi1\n",
        "accesibilty_description": ""
      }
    }
  },
  "d": {
    "f": {
      "g": {
        "text": "tit4",
        "accesibilty_description": ""
      }
    }
  },
  "language": {
    "code": "es",
    "version": "5"
  }
}
```

The script handles infinite dynamic json  depth construction. 
