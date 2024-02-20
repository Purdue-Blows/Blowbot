import { Song } from "./song";

export class SongCollection {
  title: string;
  songs: Song[];

  constructor(title: string, songs: Song[]) {
    this.title = title;
    this.songs = songs;
  }
}
