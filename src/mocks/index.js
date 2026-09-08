export const mockUser = { id: 'u-001', name: '김도윤', email: 'engineer@patentmind.ai', role: 'admin' }

export const mockSearches = [
  { id: 'PM-2408', query: '고체 전해질 기반 전고체 배터리의 열화 억제 기술', status: '완료', createdAt: '2026.08.28', count: 48, core: 6, major: 13 },
  { id: 'PM-2407', query: '실시간 라이다 센서의 노이즈 제거 알고리즘', status: '완료', createdAt: '2026.08.26', count: 31, core: 3, major: 9 },
  { id: 'PM-2406', query: '저전력 엣지 AI 추론 가속기 구조', status: '완료', createdAt: '2026.08.21', count: 74, core: 11, major: 18 },
]

export const mockResults = [
  { id: 'r-001', title: '황화물계 고체 전해질의 계면 안정화 구조', assignee: 'QuantumCell Technologies', year: 2024, tier: 'Core', score: 100, confidence: '상', designDifficulty: '상', abstract: '양극 활물질과 고체 전해질 사이에 탄성 완충층을 배치해 충방전 중 계면 저항 상승을 억제하는 기술입니다.', metrics: [
    { label: '패밀리 크기', score: 25, max: 25 },
    { label: '피인용 횟수', score: 25, max: 25 },
    { label: '청구항 수·범위', score: 15, max: 15 },
    { label: '분쟁·심판 이력', score: 20, max: 20 },
    { label: '권리 유효성', score: 15, max: 15 },
  ], claim: '고체 전해질층과 양극층 사이에 이온전도성 완충층을 포함하고, 완충층의 탄성률을 특정 범위로 제어하는 배터리 셀.' },
  { id: 'r-002', title: '전고체 셀 제조를 위한 저온 압착 공정', assignee: 'NeoVolt Labs', year: 2023, tier: 'Major', score: 58, confidence: '상', designDifficulty: '중', abstract: '저온에서 압력을 단계적으로 증가시켜 전해질 분말의 밀도와 계면 접촉을 개선하는 제조 방법입니다.', metrics: [
    { label: '패밀리 크기', score: 15, max: 25 },
    { label: '피인용 횟수', score: 18, max: 25 },
    { label: '청구항 수·범위', score: 10, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 15, max: 15 },
  ], claim: '전해질 분말을 2단계 이상의 압력 프로파일로 압착하고, 압착 후 열처리하는 제조 방법.' },
  { id: 'r-003', title: '고체 전해질 입자 표면 코팅용 유무기 복합재', assignee: 'Sungwon Materials', year: 2022, tier: 'Reference', score: 20, confidence: '중', designDifficulty: '하', abstract: '전해질 입자 표면에 유무기 복합 코팅을 형성해 수분 민감도를 낮추고 공정 안정성을 높입니다.', metrics: [
    { label: '패밀리 크기', score: 5, max: 25 },
    { label: '피인용 횟수', score: 10, max: 25 },
    { label: '청구항 수·범위', score: 5, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 0, max: 15 },
  ], claim: '황화물 입자 표면에 산화물 나노입자와 고분자 바인더를 포함하는 복합 코팅층을 형성하는 방법.' },
  { id: 'r-004', title: '배터리 팩 열관리용 냉각 플레이트', assignee: 'K-Motion', year: 2021, tier: 'Noise', score: 10, confidence: '하', designDifficulty: '하', abstract: '배터리 모듈 하부 냉각 플레이트의 유로 설계에 관한 기술입니다.', metrics: [
    { label: '패밀리 크기', score: 5, max: 25 },
    { label: '피인용 횟수', score: 0, max: 25 },
    { label: '청구항 수·범위', score: 5, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 0, max: 15 },
  ], claim: '복수의 냉각 유로가 형성된 냉각 플레이트 및 이를 포함하는 배터리 팩.' },
]
