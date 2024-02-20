import {
  SlashCommandBuilder,
  ChannelType,
  TextChannel,
  EmbedBuilder,
} from "discord.js";
import { getThemeColor } from "../functions";
import { SlashCommand } from "../types";

const command: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("get_song_info")
    // .setDescription(`
    //   Retrieve information about a song from the bot's song database. You can find songs by:
    //   - keyword/title
    //   - id
    //   - credits (composer, arranger, performer, etc)`),
    .setDescription(
      `Retrieve information about a song from the bot's song database.`
    ),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 3,
};

export default command;
