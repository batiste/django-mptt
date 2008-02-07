
from django.core.management.base import BaseCommand
from areyah.apps.categories.models import Category

from mptt.utils import drilldown_tree_for_node

class Command(BaseCommand):
    def handle(self, *args, **options):
        def rebuild_tree(node, tree_id, lft=0, level=1):
            rght = lft + 1
            print "%s%s (%s)" % ("    " * (level - 1), node.name, unicode(node.parent))
            for child in node.children.all().order_by("name"):
                rght = rebuild_tree(child, tree_id, rght, level + 1)
            node.lft, node.rght = lft, rght
            node.tree_id = tree_id
            node.level = level
            node.save()
            return rght + 1
        tree_id = 0
        for root_node in Category.tree.root_nodes().order_by("name"):
            rebuild_tree(root_node, tree_id)
            tree_id += 1
