const API_BASE_URL = "http://localhost:5050/api";

/**
 * 랭킹 조회
 * GET /api/rankings
 * 하단에 작게 '랭킹은 대시보드에서 확인할 수 있습니다.' 알림 문구 포함
 */
export async function getRankings() {
  try {
    const response = await fetch(`${API_BASE_URL}/rankings`);

    if (!response.ok) {
      throw new Error(`랭킹 조회 실패 (${response.status})`);
    }

    const data = await response.json();

    // 서버 응답 객체 구조를 안전하게 보장하며 가공 및 리턴
    return {
      rankings: data.rankings || {
        blue_red_flag: [],
        memory: [],
        red_light_green_light: []
      },
      // 랭킹 안내 문구 메타데이터 결합
      notice: data.notice || "랭킹은 대시보드에서 확인할 수 있습니다."
    };
  } catch (error) {
    console.error("[RankingService] getRankings error", error);

    return {
      rankings: {
        blue_red_flag: [],
        memory: [],
        red_light_green_light: []
      },
      notice: "랭킹은 대시보드에서 확인할 수 있습니다."
    };
  }
}

/**
 * 성장 단계 및 다마고치 상태 조회
 * GET /api/state
 * 파이썬 백엔드(state.py)의 _initial_state 스키마 필드값과 100% 매핑
 */
export async function getGrowthInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/state`);

    if (!response.ok) {
      throw new Error(`성장 정보 조회 실패 (${response.status})`);
    }

    const state = await response.json();

    // 서버 코드(state.py)가 내려주는 원본 필드 문자열 스네이크 케이스를 프론트 camelCase로 안정적으로 정제
    return {
      growthStage: state.growth_stage || "BABY", // "BABY" | "CHILD" | "ADULT"
      birthDate: state.birth_date || null,       // "YYYY-MM-DD"
      hunger: typeof state.hunger === "number" ? state.hunger : 40,
      fun: typeof state.fun === "number" ? state.fun : 40,
      energy: typeof state.energy === "number" ? state.energy : 40,
      favorability: typeof state.favorability === "number" ? state.favorability : 0,
      mood: state.mood || "NORMAL",              // "NORMAL" | "HAPPY" | "HUNGRY" 등
      isSleeping: state.is_sleeping || false
    };
  } catch (error) {
    console.error("[RankingService] getGrowthInfo error", error);

    // 에러 발생 시 state.py의 _initial_state 기본값 기준 프로토타입 리턴
    return {
      growthStage: "BABY",
      birthDate: null,
      hunger: 40,
      fun: 40,
      energy: 40,
      favorability: 0,
      mood: "NORMAL",
      isSleeping: false
    };
  }
}

/**
 * 인벤토리 조회 (선물함 항목)
 * GET /api/inventory
 * 하단에 작게 '받은 선물은 대시보드에서 확인할 수 있습니다.' 알림 문구 포함
 */
export async function getInventory() {
  try {
    const response = await fetch(`${API_BASE_URL}/inventory`);

    if (!response.ok) {
      throw new Error(`인벤토리 조회 실패 (${response.status})`);
    }

    const data = await response.json();

    return {
      gifts: data.gifts || [],
      // 선물 안내 문구 메타데이터 결합
      notice: data.notice || "받은 선물은 대시보드에서 확인할 수 있습니다."
    };
  } catch (error) {
    console.error("[RankingService] getInventory error", error);
    return {
      gifts: [],
      notice: "받은 선물은 대시보드에서 확인할 수 있습니다."
    };
  }
}

/**
 * 랭킹 + 성장정보 한번에 병렬 조회
 * 대시보드 혹은 모달 컴포넌트 렌더링에 일괄 적용
 */
export async function getRankingModalData() {
  try {
    const [rankingData, growthInfo] = await Promise.all([
      getRankings(),
      getGrowthInfo()
    ]);

    return {
      rankings: rankingData.rankings,
      notice: rankingData.notice,
      growthInfo: growthInfo
    };
  } catch (error) {
    console.error("[RankingService] getRankingModalData error", error);

    return {
      rankings: {
        blue_red_flag: [],
        memory: [],
        red_light_green_light: []
      },
      notice: "랭킹은 대시보드에서 확인할 수 있습니다.",
      growthInfo: {
        growthStage: "BABY",
        birthDate: null,
        hunger: 40,
        fun: 40,
        energy: 40,
        favorability: 0,
        mood: "NORMAL",
        isSleeping: false
      }
    };
  }
}
