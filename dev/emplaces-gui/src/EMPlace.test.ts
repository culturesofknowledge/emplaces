import { instanceOfEMPlace } from "./EMPlace";

it('is an EMPlace when all properties have a value', () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Opole Voivodeship (ADM1)"
      },
      "em_placeType": {
        "title": {
          "value": "First-order admin division"
        }
      },
      "em_alternateNameList": {
        "items": [
          {
            "value": "Voivodat d'Opole"
          },
          {
            "value": "Opolské vojvodství"
          }
        ]
      }
    }
  )).toBe(true);
});

it('is an EMPlace if the title has a value', () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Duchy of Opole"
      },
      "em_placeType": null,
      "em_alternateNameList": {
        "items": []
      }
    }
  )).toBe(true);
});

it("is not a valid EMPlace without placeType property", () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Duchy of Opole"
      },
      "em_alternateNameList": {
        "items": []
      }
    }
  )).toBe(false);
});

it('is not a valid EMPlace without em_alternateNameList property', () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Duchy of Opole"
      },
      "em_placeType": null,
    }
  )).toBe(false);
});

it('is not a valid EMPlace without em_alternateNameList items property', () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Duchy of Opole"
      },
      "em_placeType": null,
      "em_alternateNameList": {
      }
    }
  )).toBe(false);
});

it('is not a valid EMPlace without em_alternateNameList items property, that is null', () => {
  expect(instanceOfEMPlace(
    {
      "title": {
        "value": "Duchy of Opole"
      },
      "em_placeType": null,
      "em_alternateNameList": {
        "items": null
      }
    }
  )).toBe(false);
});
