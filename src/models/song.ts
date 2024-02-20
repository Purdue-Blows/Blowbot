export class Song {
  title: string;
  credits: string[];
  // {key: list of images (in case there's more than one page associated with that key)}
  refs: { string: Buffer[] };

  constructor(title: string, credits: string[], refs: { string: Buffer[] }) {
    this.title = title;
    this.credits = credits;
    this.refs = refs;
  }
}
