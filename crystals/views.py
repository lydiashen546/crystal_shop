from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Crystal, CrystalEffect, CrystalEffectRelation, ProductCrystal


def crystal_list(request):
    query = request.GET.get("q", "").strip()
    effect_id = request.GET.get("effect")
    effect_groups = []
    linked_crystal_ids = set()
    effects = CrystalEffect.objects.all()
    if effect_id:
        effects = effects.filter(id=effect_id)
    for effect in effects:
        relations = CrystalEffectRelation.objects.filter(crystal_effect=effect).select_related("crystal")
        if query:
            relations = relations.filter(
                Q(crystal__crystal_name__icontains=query)
                | Q(crystal__description__icontains=query)
                | Q(crystal__origin__icontains=query)
                | Q(crystal_effect__name__icontains=query)
                | Q(crystal_effect__description__icontains=query)
            )
        crystals = [relation.crystal for relation in relations]
        if crystals:
            linked_crystal_ids.update(crystal.id for crystal in crystals)
            effect_groups.append({"effect": effect, "crystals": crystals})

    unclassified = Crystal.objects.exclude(id__in=linked_crystal_ids).prefetch_related("images")
    if effect_id:
        unclassified = Crystal.objects.none()
    if query:
        unclassified = unclassified.filter(
            Q(crystal_name__icontains=query)
            | Q(description__icontains=query)
            | Q(origin__icontains=query)
        )
    return render(
        request,
        "crystals/list.html",
        {
            "effect_groups": effect_groups,
            "effects": CrystalEffect.objects.all(),
            "unclassified": unclassified,
            "query": query,
            "selected_effect": effect_id,
        },
    )


def crystal_detail(request, crystal_id):
    crystal = get_object_or_404(
        Crystal.objects.prefetch_related("images", "content_sections"),
        pk=crystal_id,
    )
    effect_relations = CrystalEffectRelation.objects.filter(crystal=crystal).select_related("crystal_effect")
    crystal_images = list(crystal.images.all())
    related_products = [
        relation.product
        for relation in ProductCrystal.objects.filter(crystal=crystal).select_related("product", "product__category")
    ]
    return render(
        request,
        "crystals/detail.html",
        {
            "crystal": crystal,
            "effect_relations": effect_relations,
            "crystal_images": crystal_images,
            "related_products": related_products,
        },
    )
