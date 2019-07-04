import {instanceOfOption, instanceOfFacetData, instanceOfOptionList} from './Facet'

it('is valid option', () => {
  expect(instanceOfOption({name: "name", count: 2})).toBe(true);
});

it('is valid option[]', () => {
  expect(instanceOfOptionList([{name: "name", count: 2}])).toBe(true);
});

it('is valid FacetData', () => {
  expect(instanceOfFacetData({caption: "caption", "options": [{name: "name", count: 2}]})).toBe(true);
});