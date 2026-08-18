import unreal

_level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
_on_map_opened = _level_editor.on_map_opened


def enable_anim_update(map_name="", is_template=False):
	unreal.log(f"[anim-in-editor] map opened: {map_name}")

	actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
	count = 0

	for actor in actor_subsystem.get_all_level_actors():
		for component in actor.get_components_by_class(unreal.SkeletalMeshComponent):
			# Use the UFUNCTION rather than set_editor_property: bUpdateAnimationInEditor is
			# EditInstanceOnly, so the property path refuses to write it on component templates.
			# The function has no such check and no-ops on unregistered components.
			try:
				component.set_update_animation_in_editor(True)
				count += 1
			except Exception as error:
				unreal.log_warning(f"[anim-in-editor] skipped {actor.get_name()}.{component.get_name()}: {error}")

	unreal.log(f"[anim-in-editor] enabled on {count} skeletal mesh component(s)")

	# Other stuff we want
	editor_world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
	unreal.SystemLibrary.execute_console_command(editor_world, "ShowFlag.Splines 0")

_on_map_opened.add_callable(enable_anim_update)

enable_anim_update(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name())
