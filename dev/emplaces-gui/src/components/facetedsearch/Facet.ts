export class FacetData {
  "caption": string
  "options": Option[]
}

class Option {
  "name": string
  "count": number
}

export class Facet {
  caption: string;
  options: Option[];
  updateListener: Function;
  selectedOptions: string[]

  constructor(data: FacetData, updateListener: Function) {
    this.caption = data.caption;
    this.options = data.options;
    this.updateListener = updateListener;
    this.selectedOptions = [];

  }

  optionSelected(option: string) {
    this.selectedOptions.push(option);
    this.updateListener();
  }
}

export function instanceOfFacetData(object: any): object is FacetData {
  return typeof (object["caption"]) === 'string' && instanceOfOptionList(object["options"]);
}

export function instanceOfOptionList(object: any): object is Option[] {
  return object instanceof Array && object.every(item => instanceOfOption(item));
}

export function instanceOfOption(object: any): object is Option {
  return typeof object["name"] === 'string' && typeof object["count"] === 'number';
}

