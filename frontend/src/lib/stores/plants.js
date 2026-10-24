import { writable } from 'svelte/store';

// 기본 목업 식물 컬렉션 (시각적 프리뷰용)
export const initialPlants = [
  {
    id: 1,
    nickname: '초록이',
    species: 'Monstera Deliciosa',
    common_name: '몬스테라 델리시오사',
    scientific_name: 'Monstera deliciosa',
    image_path: 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=600&q=80',
    created_at: '2026-10-20',
    care_guide: {
      watering: '겉흙이 마르면 듬뿍 주기 (주 1~2회)',
      light: '밝은 간접광 선호',
      temperature: '18~27°C',
      soil: '배수가 잘 되는 관엽토',
      fertilizer: '생장기(봄~가을) 월 1회',
      notes: '잎을 주기적으로 닦아주고 과습을 주의하세요'
    }
  },
  {
    id: 2,
    nickname: '금전수 대박이',
    species: 'Zamioculcas zamiifolia',
    common_name: '금전수 (자미오쿨카스)',
    scientific_name: 'Zamioculcas zamiifolia',
    image_path: 'https://images.unsplash.com/photo-1632207691143-643e2a9a9361?auto=format&fit=crop&w=600&q=80',
    created_at: '2026-10-22',
    care_guide: {
      watering: '속흙까지 바짝 마르면 관수 (월 1~2회)',
      light: '반음지~반양지 적응력 우수',
      temperature: '16~26°C',
      soil: '마사토를 섞은 배수성 좋은 흙',
      fertilizer: '봄철 1~2회 미량 공급',
      notes: '건조에 매우 강하며 과습은 뿌리를 썩게 합니다'
    }
  },
  {
    id: 3,
    nickname: '포토스',
    species: 'Epipremnum aureum',
    common_name: '스킨답서스 (골든 포토스)',
    scientific_name: 'Epipremnum aureum',
    image_path: 'https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?auto=format&fit=crop&w=600&q=80',
    created_at: '2026-10-24',
    care_guide: {
      watering: '흙 표면이 마르면 공급 (주 1회 내외)',
      light: '은은한 간접광 또는 형광등 조명',
      temperature: '18~24°C',
      soil: '일반 분갈이용 배양토',
      fertilizer: '액체 비료 2달에 1회',
      notes: '수경재배로도 매우 잘 자라며 공기정화 능력이 뛰어납니다'
    }
  }
];

// 현재 분석된 결과 스토어
export const currentResult = writable({
  species: 'Monstera Deliciosa',
  common_name: '몬스테라 델리시오사',
  scientific_name: 'Monstera deliciosa',
  confidence: 0.94,
  imageUrl: 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=800&q=80',
  candidates: [
    { species: 'Monstera Deliciosa', common_name: '몬스테라 델리시오사', scientific_name: 'Monstera deliciosa', confidence: 0.94 },
    { species: 'Epipremnum aureum', common_name: '스킨답서스 (골든 포토스)', scientific_name: 'Epipremnum aureum', confidence: 0.78 },
    { species: 'Philodendron hederaceum', common_name: '하트리프 필로덴드론', scientific_name: 'Philodendron hederaceum', confidence: 0.65 }
  ],
  care_guide: {
    watering: '겉흙이 마르면 충분히 관수 (주 1~2회, 계절별 조절)',
    light: '밝은 간접광 (직사광선은 잎을 태울 수 있습니다)',
    temperature: '18~27°C (최저 13°C 이상 유지 권장)',
    soil: '배수가 원활한 관엽식물 전용 배양토 + 펄라이트 배합',
    fertilizer: '봄~가을 성장기 동안 액체 비료를 월 1회 공급',
    notes: '잎에 묻은 먼지는 미온수로 닦아 호흡을 돕고, 반려동물 섭취에 유의하세요.'
  }
});

// 내 식물 컬렉션 스토어
export const plantCollection = writable(initialPlants);

// 전역 로딩 상태
export const isLoading = writable(false);

// 현재 활성화 탭 ('identify' | 'collection')
export const activeTab = writable('identify');
