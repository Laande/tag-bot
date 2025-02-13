from discord import app_commands, Interaction
from typing import List
from .database import TagDatabase

class TagCommands:
    def __init__(self, db: TagDatabase):
        self.db = db

    async def tag_autocomplete(self, interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
        user_tags = self.db.get_user_tags(interaction.user.id)
        return [app_commands.Choice(name=tag, value=tag) for tag in user_tags if current.lower() in tag.lower()][:25]

    def setup_commands(self, tree: app_commands.CommandTree):
        tag_group = app_commands.Group(name="tag", description="Create, store, and use predefined text snippets instantly")
        tree.add_command(tag_group)

        @tag_group.command(name="create", description="Create a new predefined text snippet")
        @app_commands.describe(name="Name of the tag", content="Content of the tag")
        async def create_tag(interaction: Interaction, name: str, content: str):
            existing_tags = self.db.get_user_tags(interaction.user.id)
            if name in existing_tags:
                await interaction.response.send_message(f"Tag '{name}' already exists!", ephemeral=True)
                return
            
            self.db.add_tag(interaction.user.id, name, content)
            await interaction.response.send_message(f"Tag '{name}' created successfully!", ephemeral=True)

        @tag_group.command(name="edit", description="Edit an existing text snippet")
        @app_commands.describe(name="Name of the tag to edit", new_content="New content for the tag")
        @app_commands.autocomplete(name=self.tag_autocomplete)
        async def edit_tag(interaction: Interaction, name: str, new_content: str):
            content = self.db.get_tag_content(interaction.user.id, name)
            if not content:
                await interaction.response.send_message(f"Tag '{name}' doesn't exist!", ephemeral=True)
                return
            
            self.db.update_tag(interaction.user.id, name, new_content)
            await interaction.response.send_message(f"Tag '{name}' updated successfully!", ephemeral=True)

        @tag_group.command(name="delete", description="Delete an existing text snippet")
        @app_commands.describe(name="Name of the tag to delete")
        @app_commands.autocomplete(name=self.tag_autocomplete)
        async def delete_tag(interaction: Interaction, name: str):
            content = self.db.get_tag_content(interaction.user.id, name)
            if not content:
                await interaction.response.send_message(f"Tag '{name}' doesn't exist!", ephemeral=True)
                return
            
            self.db.delete_tag(interaction.user.id, name)
            await interaction.response.send_message(f"Tag '{name}' deleted successfully!", ephemeral=True)

        @tag_group.command(name="send", description="Send the content of a text snippet")
        @app_commands.describe(name="Name of the tag to send")
        @app_commands.autocomplete(name=self.tag_autocomplete)
        async def send_tag(interaction: Interaction, name: str):
            content = self.db.get_tag_content(interaction.user.id, name)
            if not content:
                await interaction.response.send_message(f"Tag '{name}' doesn't exist!", ephemeral=True)
                return
            
            await interaction.response.send_message(content)