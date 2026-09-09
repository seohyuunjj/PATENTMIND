export const mockUser = { id: 'u-001', name: 'Seo', email: 'engineer@patentmind.ai', role: 'admin' }

export const mockSearches = [
  { id: 'PM-2409', query: 'AI 가속기용 HBM(고대역폭 메모리) 적층 패키징 및 TSV·인터포저 기술', status: '완료', createdAt: '2026.09.09', count: 9, core: 2, major: 3 },
  { id: 'PM-2408', query: '고체 전해질 기반 전고체 배터리의 열화 억제 기술', status: '완료', createdAt: '2026.08.28', count: 48, core: 6, major: 13 },
  { id: 'PM-2407', query: '실시간 라이다 센서의 노이즈 제거 알고리즘', status: '완료', createdAt: '2026.08.26', count: 31, core: 3, major: 9 },
  { id: 'PM-2406', query: '저전력 엣지 AI 추론 가속기 구조', status: '완료', createdAt: '2026.08.21', count: 74, core: 11, major: 18 },
]

// 검색어 "AI 가속기용 HBM(고대역폭 메모리) 적층 패키징 및 TSV·인터포저 기술"로 조회한 실제 공개/등록 특허 9건.
// 출처: Google Patents (patents.google.com). 정량 5대 지표 점수는 패밀리 크기·인용 정보 등 조회 가능한 실제 신호를 참고해
// AI가 합리적으로 추정한 상대 점수이며(실시간 심판·소송 DB 연동 전 단계), 실제 서비스에서는 KIPRIS/특허청 API로 대체될 값입니다.
export const mockResults = [
  { id: 'r-001', title: '[US11133282B2] CoWoS(Chip-on-Wafer-on-Substrate) 패키지 구조 및 형성 방법', assignee: 'Taiwan Semiconductor Manufacturing Co. (TSMC)', year: 2021, tier: 'Core', score: 96, confidence: '상', designDifficulty: '상', abstract: 'TSV(관통 실리콘 비아)를 포함한 인터포저에 다이를 접합한 뒤 박막화·재배선(RDL)으로 완성하는 CoWoS 패키지 구조로, HBM-로직 다이 간 고대역폭 연결의 표준 패키징 방식으로 자리잡은 TSMC의 핵심 특허입니다.', metrics: [
    { label: '패밀리 크기', score: 25, max: 25 },
    { label: '피인용 횟수', score: 24, max: 25 },
    { label: '청구항 수·범위', score: 14, max: 15 },
    { label: '분쟁·심판 이력', score: 18, max: 20 },
    { label: '권리 유효성', score: 15, max: 15 },
  ], claim: '인터포저 상에 관통 비아를 형성하고 디바이스 다이를 접합한 후, 인터포저를 박막화하여 관통 비아를 노출시키고 재배선층을 통해 기판과 연결하는 반도체 패키지 형성 방법.' },
  { id: 'r-002', title: '[US11955408B2] 관통 실리콘 비아(TSV)를 포함하는 집적회로 반도체 소자', assignee: 'Samsung Electronics', year: 2024, tier: 'Core', score: 86, confidence: '상', designDifficulty: '상', abstract: '하부가 상부보다 넓은 랜딩 구조의 TSV를 적용해 적층 다이 간 전기적 접속 신뢰성을 높인 구조로, HBM 적층 메모리의 다이 간 수직 연결 신뢰성과 직결되는 최신 구조 특허입니다.', metrics: [
    { label: '패밀리 크기', score: 23, max: 25 },
    { label: '피인용 횟수', score: 20, max: 25 },
    { label: '청구항 수·범위', score: 13, max: 15 },
    { label: '분쟁·심판 이력', score: 16, max: 20 },
    { label: '권리 유효성', score: 14, max: 15 },
  ], claim: '제1 표면으로부터 이격된 제1 부분과 그보다 폭이 넓은 제2 부분을 갖는 TSV 랜딩부를 포함하는 집적회로 반도체 장치.' },
  { id: 'r-003', title: '[US9911465B1] HBM 대역폭 통합 스위치 (Bandwidth Aggregation Switch)', assignee: 'Xilinx, Inc.', year: 2018, tier: 'Major', score: 61, confidence: '상', designDifficulty: '중', abstract: '인터포저를 통해 프로그래머블 IC와 HBM 다이 사이에 스위치 네트워크를 갖는 인터페이스 다이를 배치해, 실제 FPGA 제품(Virtex UltraScale+ HBM)에 적용된 HBM 인터포저 연결 구조입니다.', metrics: [
    { label: '패밀리 크기', score: 14, max: 25 },
    { label: '피인용 횟수', score: 16, max: 25 },
    { label: '청구항 수·범위', score: 10, max: 15 },
    { label: '분쟁·심판 이력', score: 8, max: 20 },
    { label: '권리 유효성', score: 13, max: 15 },
  ], claim: '인터포저 상에서 프로그래머블 집적회로 다이와 HBM 다이 사이에 스위치 네트워크를 갖는 인터페이스 다이를 개재하여 연결하는 반도체 장치.' },
  { id: 'r-004', title: '[CN113488449A] 고대역폭 메모리용 집적회로 패키지 (HBM3 기판 트레이스 방식)', assignee: 'Google LLC', year: 2021, tier: 'Major', score: 51, confidence: '중', designDifficulty: '중', abstract: 'HBM3 세대의 넓어진 마이크로범프 피치(96μm)를 활용해 실리콘 인터포저 배선 일부를 저비용 기판 트레이스로 대체, 인터포저 면적과 원가를 줄이는 대안 패키징 구조입니다. (US/EP/CN 3개국 패밀리)', metrics: [
    { label: '패밀리 크기', score: 12, max: 25 },
    { label: '피인용 횟수', score: 13, max: 25 },
    { label: '청구항 수·범위', score: 9, max: 15 },
    { label: '분쟁·심판 이력', score: 5, max: 20 },
    { label: '권리 유효성', score: 12, max: 15 },
  ], claim: '로직 다이 하부에만 인터포저를 배치하고 HBM 스택과 로직 다이 사이 일부 배선을 기판의 유기 트레이스로 대체한 집적회로 패키지.' },
  { id: 'r-005', title: '[US11398453B2] AI 가속기용 HBM 실리콘 포토닉 TSV 아키텍처 (룩업 컴퓨팅)', assignee: 'Samsung Electronics', year: 2022, tier: 'Major', score: 49, confidence: '중', designDifficulty: '하', abstract: '룩업 테이블을 갖는 메모리 다이와 로직 다이를 광학 비아로 연결해 AI 가속 연산의 데이터 전송 대역폭을 높이는 구조로, HBM TSV 응용 중에서도 광 인터커넥트에 특화된 니치 기술입니다.', metrics: [
    { label: '패밀리 크기', score: 13, max: 25 },
    { label: '피인용 횟수', score: 11, max: 25 },
    { label: '청구항 수·범위', score: 8, max: 15 },
    { label: '분쟁·심판 이력', score: 4, max: 20 },
    { label: '권리 유효성', score: 13, max: 15 },
  ], claim: '룩업 테이블을 포함하는 메모리 회로 다이와 조합 논리 회로를 포함하는 로직 다이 사이를 광학 비아로 결합한 AI 가속 장치.' },
  { id: 'r-006', title: '[US12182040B1] 세대 간 호환을 위한 스케일러블 HBM 멀티칩 모듈', assignee: 'Eliyan Corp.', year: 2024, tier: 'Reference', score: 29, confidence: '중', designDifficulty: '하', abstract: 'N/2 채널을 지원하는 구세대 HBM 2개를 결합해 신세대 HBM과 동일한 총 채널·대역폭을 내는 구조로, 기존 프로세서 설계를 그대로 재사용할 수 있게 합니다. 2024년 말 등록으로 아직 피인용 데이터가 거의 없습니다.', metrics: [
    { label: '패밀리 크기', score: 6, max: 25 },
    { label: '피인용 횟수', score: 3, max: 25 },
    { label: '청구항 수·범위', score: 7, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 13, max: 15 },
  ], claim: '각각 N/2 채널을 지원하는 두 개의 레거시 HBM 장치를 결합하여 N개 채널의 집계 대역폭을 제공하는 멀티칩 모듈.' },
  { id: 'r-007', title: '[US20140057434A1] 관통 실리콘 비아(TSV) 공정 (범용 패시베이션 공정)', assignee: 'United Microelectronics Corp. (UMC)', year: 2014, tier: 'Reference', score: 22, confidence: '하', designDifficulty: '하', abstract: '웨이퍼 이면에 패시베이션층을 먼저 형성해 산화막 두께를 제어함으로써 디척킹·틀어짐 등 웨이퍼 핸들링 불량을 줄이는 범용 TSV 공정으로, HBM에 국한되지 않는 공정 특허입니다. (패밀리 2건: 본 출원 + US9012324B2)', metrics: [
    { label: '패밀리 크기', score: 5, max: 25 },
    { label: '피인용 횟수', score: 8, max: 25 },
    { label: '청구항 수·범위', score: 6, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 3, max: 15 },
  ], claim: '기판 이면에 패시베이션층을 형성한 후 그 위에 산화막을 형성하여 산화막 두께를 제한하는 관통 실리콘 비아 공정.' },
  { id: 'r-008', title: '[US20070247936A1] 고대역폭 수신기를 위한 유연한 메모리 활용 구조', assignee: 'Texas Instruments Inc.', year: 2007, tier: 'Noise', score: 7, confidence: '하', designDifficulty: '하', abstract: '"high bandwidth"와 "memory" 키워드는 일치하지만 실제로는 방송 수신기의 도플러 보정·MPE-FEC 기능 간 메모리 공간을 동적으로 배분하는 신호처리 기술로, 반도체 적층·패키징과는 무관합니다. 등록(B2)으로 이어지지 않은 출원으로 확인됩니다.', metrics: [
    { label: '패밀리 크기', score: 3, max: 25 },
    { label: '피인용 횟수', score: 2, max: 25 },
    { label: '청구항 수·범위', score: 2, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 0, max: 15 },
  ], claim: '도플러 보정과 MPE-FEC 기능이 메모리 공간을 경쟁적으로 할당받도록 구성 가능한 수신기용 메모리 회로.' },
  { id: 'r-009', title: '[US4875206A] 고대역폭 인터리브 버퍼 메모리 및 제어 (1989, 통신망)', assignee: 'AT&T Bell Laboratories', year: 1989, tier: 'Noise', score: 7, confidence: '하', designDifficulty: '하', abstract: '"고대역폭 버퍼 메모리" 키워드는 일치하지만 실제로는 광섬유 기반 대도시 통신망(MAN)의 데이터 스위칭 버퍼 기술로, 반도체 다이 적층·패키징과 무관한 1980년대 통신 특허입니다. 존속기간이 만료되어 권리 유효성이 없습니다.', metrics: [
    { label: '패밀리 크기', score: 2, max: 25 },
    { label: '피인용 횟수', score: 3, max: 25 },
    { label: '청구항 수·범위', score: 2, max: 15 },
    { label: '분쟁·심판 이력', score: 0, max: 20 },
    { label: '권리 유효성', score: 0, max: 15 },
  ], claim: '인터리브 버퍼 저장 및 동기식 데이터 링 구조를 사용해 대도시 통신망의 데이터 트래픽을 스위칭하는 방법.' },
]
