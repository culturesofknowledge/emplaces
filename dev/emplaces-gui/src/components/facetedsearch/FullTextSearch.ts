export default class FullTextSearch {
  term: string;
  updateListener: Function;
  constructor(updateListener: Function) {
    this.term = "";
    this.updateListener = updateListener
  }

  search(term: string) {
    this.term = term;
    this.updateListener();
  }
}