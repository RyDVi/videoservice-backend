from rest_framework import serializers

class ChildListSerializer(serializers.ListSerializer):
    def on_update_delete(self, queryset):
        queryset.delete()

    def update(self, instance, validated_data):
        instances = instance
        instances_mapping = {i.id: i for i in instances}
        created_updated_instances = []

        self.on_update_delete(
            instances.exclude(id__in=[i["id"]
                              for i in validated_data if i.get("id")])
        )
        for instance_data in validated_data:
            pk = instance_data.pop("id", None)
            try:
                instance = instances_mapping[pk]
            except KeyError:
                instance = self.child.create(instance_data)
            else:
                instance = self.child.update(instance, instance_data)
            created_updated_instances.append(instance)
        return created_updated_instances


class ChildListNoDeleteSerializer(ChildListSerializer):
    def on_update_delete(self, queryset):
        pass
