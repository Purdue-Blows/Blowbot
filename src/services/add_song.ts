import { Key } from "../utils/keys";
import { collection_to_string } from "../utils/collections";
import { KeySelection } from "../components/key_button";

function add_song(
  collection: string,
  title: string,
  refs: KeySelection,
  composer: string[] | null,
  arranger: string[] | null,
  performer: string[] | null
) {
  // Function logic here
  collection = collection_to_string(collection);
  // TODO: write to collection
}

export default add_song;
