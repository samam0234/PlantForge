"""Houseplant catalog used by the local identifier and care-guide fallback.

Profiles are color features in 0..1 (warmth is mean(R-B)/255, typically -0.4..0.4).
They are reference points, not a trained model. OpenAI Vision replaces this path
when AI_PROVIDER=openai (or auto) and OPENAI_API_KEY is set.
"""

PLANTS = [
    {
        "species": "Monstera deliciosa",
        "common_name": "몬스테라",
        "scientific_name": "Monstera deliciosa",
        "profile": {
            "green_ratio": 1.0,
            "brightness": 0.24,
            "saturation": 0.715,
            "contrast": 0.096,
            "warmth": -0.092,
        },
        "care_guide": {
            "watering": "겉흙 2~3cm가 마르면 화분 아래로 물이 빠질 때까지 흠뻑 줍니다. 봄·여름은 주 1~2회, 겨울은 2주에 1회 정도로 줄이세요.",
            "light": "밝은 간접광이 적당합니다. 직사광선은 잎을 태우므로 얇은 커튼 너머의 창가가 좋습니다.",
            "temperature": "18~27°C. 13°C 아래로 내려가면 생장이 멈추고 냉해를 입을 수 있습니다.",
            "soil": "배수 구멍이 있는 화분에 관엽 배양토와 펄라이트(또는 바크)를 7:3 정도로 섞어 사용합니다.",
            "fertilizer": "4~9월 성장기에 액체 비료를 권장 농도의 절반으로 희석해 월 1회 줍니다. 겨울에는 쉬세요.",
            "notes": "잎의 구멍(fenestration)은 빛이 충분할 때 잘 생깁니다. 수액에 수산칼슘이 있어 반려동물과 어린이 섭취에 주의하세요.",
            "seasonal_tip": "봄에 뿌리가 화분 바닥으로 나오면 한 치수 큰 화분으로 분갈이하고, 공중뿌리는 자르지 말고 이끼로 습도를 유지해 주세요.",
        },
    },
    {
        "species": "Epipremnum aureum",
        "common_name": "스킨답서스",
        "scientific_name": "Epipremnum aureum",
        "profile": {
            "green_ratio": 0.156,
            "brightness": 0.776,
            "saturation": 0.361,
            "contrast": 0.139,
            "warmth": 0.235,
        },
        "care_guide": {
            "watering": "겉흙이 마르면 줍니다. 주 1회 전후가 보통이며, 잎이 축 처지면 목이 마른 신호입니다. 화분 받침의 고인 물은 버리세요.",
            "light": "밝은 간접광에서 무늬가 선명합니다. 너무 어두우면 노란 무늬가 사라지고 잎이 작아집니다.",
            "temperature": "18~28°C. 찬 바람과 에어컨 송풍구 바로 앞은 피합니다.",
            "soil": "일반 배양토로 충분합니다. 줄기를 물에 담가 수경재배로 키울 수도 있습니다.",
            "fertilizer": "성장기 6~8주에 한 번 묽은 액체 비료를 줍니다. 수경이면 수경용 양액을 사용하세요.",
            "notes": "공기정화 식물로 알려져 있지만 잎과 줄기는 반려동물에게 독성이 있습니다. 어린 순이 잘리면 칼슘옥살레이트 결정이 자극을 줍니다.",
            "seasonal_tip": "가을에 줄기가 웃자라면 마디 아래로 잘라 물꽂이하면 쉽게 번식합니다. 겨울에는 물을 더 말리고 창에서 한 걸음 안쪽으로 두세요.",
        },
    },
    {
        "species": "Echeveria elegans",
        "common_name": "에케베리아",
        "scientific_name": "Echeveria elegans",
        "profile": {
            "green_ratio": 0.629,
            "brightness": 0.829,
            "saturation": 0.098,
            "contrast": 0.083,
            "warmth": -0.027,
        },
        "care_guide": {
            "watering": "흙이 완전히 마른 뒤 저면관수하거나 잎에 물이 닿지 않게 흙에만 줍니다. 여름·겨울 휴면기에는 월 1회 이하로 줄이세요.",
            "light": "하루 4시간 이상 밝은 빛, 가능하면 직사광이 필요합니다. 빛이 부족하면 줄기가 웃자랍니다.",
            "temperature": "15~28°C. 5°C 이하에서는 실내로 들이고, 한여름 한낮의 강한 직광은 차광해 주세요.",
            "soil": "마사토·펄라이트 비율이 높은 다육 전용토를 사용합니다. 일반 배양토만 쓰면 쉽게 과습됩니다.",
            "fertilizer": "봄·가을 성장기에만 다육 비료를 아주 옅게 한 번 줍니다. 자주 주면 웃자라며 형태가 무너집니다.",
            "notes": "잎 중앙에 물이 고이면 썩습니다. 반려동물이 먹어도 대체로 독성은 낮지만, 관상용으로 두고 섭취는 막으세요.",
            "seasonal_tip": "장마철에는 비를 맞지 않게 하고 선풍기로 통풍을 확보하세요. 아래잎이 마르는 것은 자연스러운 하엽입니다.",
        },
    },
    {
        "species": "Zamioculcas zamiifolia",
        "common_name": "금전수",
        "scientific_name": "Zamioculcas zamiifolia",
        "profile": {
            "green_ratio": 0.8,
            "brightness": 0.18,
            "saturation": 0.35,
            "contrast": 0.1,
            "warmth": -0.12,
        },
        "care_guide": {
            "watering": "속흙까지 마른 뒤에만 줍니다. 보통 2~4주에 한 번이면 충분하고, 과습은 알뿌리(괴경)를 썩게 합니다.",
            "light": "반음지에서도 견디지만 밝은 간접광에서 더 튼튼합니다. 직사광은 잎을 노랗게 태울 수 있습니다.",
            "temperature": "16~26°C. 10°C 이하로 오래 두면 잎이 떨어집니다.",
            "soil": "배수성이 좋은 관엽토에 마사토를 섞습니다. 화분은 꼭 배수 구멍이 있어야 합니다.",
            "fertilizer": "봄에 1~2회, 묽은 액체 비료면 충분합니다. 비료가 적어도 잘 자랍니다.",
            "notes": "전초가 독성이 있어 반려동물 섭취에 주의하세요. 잎이 갑자기 노랗게 무너지면 대부분 물 과다입니다.",
            "seasonal_tip": "겨울에는 거의 물을 끊다시피 하고, 분갈이는 2~3년에 한 번 봄에만 하세요. 괴경을 나눠 번식할 수 있습니다.",
        },
    },
    {
        "species": "Dracaena trifasciata",
        "common_name": "산세베리아",
        "scientific_name": "Dracaena trifasciata",
        "profile": {
            "green_ratio": 0.48,
            "brightness": 0.33,
            "saturation": 0.32,
            "contrast": 0.28,
            "warmth": -0.02,
        },
        "care_guide": {
            "watering": "흙이 바짝 마른 뒤 듬뿍, 그리고 다시 완전히 마를 때까지 기다립니다. 겨울에는 월 1회면 충분한 경우가 많습니다.",
            "light": "밝은 곳부터 약한 그늘까지 적응합니다. 무늬종은 너무 어두우면 줄무늬가 옅어집니다.",
            "temperature": "15~29°C. 찬 창가에 잎이 직접 닿지 않게 하세요.",
            "soil": "선인장·다육 배합토처럼 물 빠짐이 빠른 흙이 안전합니다.",
            "fertilizer": "봄·여름에 2개월에 한 번 묽은 관엽 비료를 줍니다.",
            "notes": "잎 끝이 마르면 공기가 너무 건조하거나 물을 불규칙하게 준 경우가 많습니다. 사포닌 성분이 있어 반려동물 섭취는 피하세요.",
            "seasonal_tip": "잎꽂이로 번식할 수 있지만 무늬는 사라질 수 있습니다. 무늬를 유지하려면 뿌리줄기를 나눠 심으세요.",
        },
    },
    {
        "species": "Ficus lyrata",
        "common_name": "떡갈고무나무",
        "scientific_name": "Ficus lyrata",
        "profile": {
            "green_ratio": 0.66,
            "brightness": 0.3,
            "saturation": 0.3,
            "contrast": 0.12,
            "warmth": -0.04,
        },
        "care_guide": {
            "watering": "겉흙이 마르면 충분히 주고 받침 물은 버립니다. 물을 주고 자리를 옮기면 잎을 떨구는 일이 많습니다.",
            "light": "밝은 간접광이 필요합니다. 창문에서 1~2m 안쪽, 직사광은 오전의 부드러운 빛만 허용하세요.",
            "temperature": "18~27°C. 위치와 온도가 자주 바뀌면 낙엽이 옵니다.",
            "soil": "배수가 좋은 관엽 배양토. 분갈이 직후 일주일은 물을 살짝 아껴 뿌리를 안정시킵니다.",
            "fertilizer": "성장기 월 1회 액체 비료. 새 잎이 나올 때 농도를 더 옅게 주세요.",
            "notes": "잎의 먼지를 젖은 천으로 닦아야 광합성이 유지됩니다. 수액이 피부에 자극을 줄 수 있고 반려동물에게 독성이 있습니다.",
            "seasonal_tip": "겨울철 난방으로 공기가 건조하면 잎 가장자리가 갈색으로 탑니다. 가습기나 자갈 물접시로 습도를 보완하세요.",
        },
    },
    {
        "species": "Spathiphyllum wallisii",
        "common_name": "스파티필름",
        "scientific_name": "Spathiphyllum wallisii",
        "profile": {
            "green_ratio": 0.5,
            "brightness": 0.4,
            "saturation": 0.26,
            "contrast": 0.22,
            "warmth": -0.01,
        },
        "care_guide": {
            "watering": "흙이 마르기 전에 촉촉하게 유지합니다. 잎이 축 처지면 물을 달라는 신호이니, 그때 흠뻑 주면 대개 몇 시간 안에 회복합니다.",
            "light": "밝은 그늘~간접광. 직사광은 잎을 탈색시킵니다. 너무 어두우면 흰 꽃이 잘 나오지 않습니다.",
            "temperature": "18~26°C. 찬 공기에 민감합니다.",
            "soil": "보수력과 배수가 둘 다 있는 관엽토. 이탄이 많은 배합이 잘 맞습니다.",
            "fertilizer": "꽃눈이 생기는 봄·여름에 월 1회 묽은 비료. 겨울에는 중단합니다.",
            "notes": "수산칼슘 결정이 있어 고양이·개가 잎을 씹으면 구강 자극이 있습니다. 잎 끝이 갈색이면 과비료이거나 물이 불규칙한 경우가 많습니다.",
            "seasonal_tip": "시든 꽃대는 밑동까지 잘라 주면 다음 꽃이 날 자리를 만듭니다. 봄에 포기를 나눠 번식하세요.",
        },
    },
    {
        "species": "Chlorophytum comosum",
        "common_name": "접란",
        "scientific_name": "Chlorophytum comosum",
        "profile": {
            "green_ratio": 0.4,
            "brightness": 0.58,
            "saturation": 0.22,
            "contrast": 0.24,
            "warmth": 0.0,
        },
        "care_guide": {
            "watering": "겉흙이 마르면 충분히 줍니다. 주 1회가 기준이고, 잎 끝이 갈색으로 마르면 물 속 불소·건조한 공기를 의심하세요.",
            "light": "밝은 간접광에서 흰 줄무늬가 선명합니다. 어두운 곳에서는 초록 비율이 늘어납니다.",
            "temperature": "15~26°C. 가벼운 서늘함에는 강하지만 서리에는 약합니다.",
            "soil": "일반 배양토면 충분합니다. 뿌리가 통통해지면 분갈이 신호입니다.",
            "fertilizer": "성장기 월 1회 묽은 액체 비료. 과하면 잎끝이 탑니다.",
            "notes": "반려동물에게 비교적 안전한 실내 식물로 많이 키웁니다. 그래도 대량 섭취는 피하세요.",
            "seasonal_tip": "길게 나온 런너의 작은 포기(자구)를 물에 꽂거나 바로 흙에 심으면 쉽게 늘릴 수 있습니다.",
        },
    },
]

GENERIC_GUIDE = {
    "watering": "겉흙이 마른 뒤 흠뻑 주고, 화분 받침에 고인 물은 비워 과습을 피하세요.",
    "light": "대부분의 실내 식물은 직사광을 피한 밝은 간접광이 안전합니다.",
    "temperature": "18~26°C를 유지하고 차가운 외풍을 피하세요.",
    "soil": "배수 구멍이 있는 화분과 관엽 배양토를 기본으로 하되, 다육이라면 마사 비율을 높이세요.",
    "fertilizer": "봄부터 가을까지 월 1회 묽은 액체 비료, 겨울에는 중단하는 편이 안전합니다.",
    "notes": "식별 신뢰도가 낮습니다. 잎과 화분이 함께 보이게 다시 촬영하면 더 정확해집니다. 반려동물 동반 가정이면 종을 확인하기 전에는 섭취를 막으세요.",
    "seasonal_tip": "계절이 바뀌면 물 주는 간격을 먼저 조절하세요. 성장기보다 겨울에 물을 줄이는 것이 대부분의 실내 식물에 맞습니다.",
}


def find_plant(scientific_name="", species="", common_name=""):
    keys = {
        (scientific_name or "").strip().lower(),
        (species or "").strip().lower(),
        (common_name or "").strip().lower(),
    }
    keys.discard("")
    for plant in PLANTS:
        names = {
            plant["scientific_name"].lower(),
            plant["species"].lower(),
            plant["common_name"].lower(),
        }
        if keys & names:
            return plant
    return None


def guide_for(scientific_name="", species="", common_name=""):
    plant = find_plant(scientific_name, species, common_name)
    if plant:
        return dict(plant["care_guide"])
    guide = dict(GENERIC_GUIDE)
    label = common_name or species or "이 식물"
    guide["notes"] = f"{label}에 대한 일반 실내 관리 기준입니다. " + guide["notes"]
    return guide
