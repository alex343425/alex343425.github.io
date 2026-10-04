# オトギフロンティア SkillEffect 參數對照

本文件整理 Release710 客戶端中 Grm.BattleEngine.Models.SkillEffect 的欄位、列舉值與旗標。

## 資料可信度與閱讀方式

- 「英文列舉名、數值、欄位型別」直接來自目前工作區的 dump.cs，可視為客戶端靜態資料所確認。
- 「中文效果」主要依列舉名翻譯；少數名稱只能表示大致用途，實際公式、套用順序與特殊條件仍要查 Build.wasm 或實戰紀錄。
- dump.cs 是 IL2CPP 產生的型別／中繼資料骨架，不是遊戲原始 C# 程式碼。它適合確認名稱、欄位與列舉，不足以單獨證明計算公式。
- 一般 enum 一次通常只取一個值；標有 [Flags] 的欄位可用位元 OR 組合，例如 5 = 1 + 4。
- JSON 中的 null 通常表示該效果未使用此欄位，不能自動當成 0。
- 未定義的數字應保留為未知值，不應自行套用相鄰數字的效果。
- &#x9; 只是 HTML 編碼的 Tab 空白，與技能效果無關。

主要靜態來源：

- [dump.cs](otogi_socket_analysis/Il2CppDumper/dump.cs)
- SkillEffectTypes：dump.cs 約第 473426–473503 行
- 各種 EffectFlags：dump.cs 約第 473508–473648 行
- SkillEffectModifiers／SkillEffectDurationModes：dump.cs 約第 473651–473670 行
- SkillEffectIconFlags：dump.cs 約第 473937–473945 行
- SkillEffect 資料模型：dump.cs 約第 475645–475718 行

## SkillEffect 欄位

| 欄位 | 型別 | 意義 |
|---|---|---|
| Id | int | 這一筆技能效果的唯一 ID。 |
| Order | int | 同一技能內的效果順序；可能影響處理或顯示順序。 |
| SkillRef | Skill | 所屬技能的參照。MasterData JSON 不一定直接輸出完整物件。 |
| SkillEffectType | SkillEffectTypes | 效果種類，完整數值表見下方。 |
| SkillEffectModifier | SkillEffectModifiers | 效果方向，例如上升、下降或耐性增減。 |
| Attribute | Attribute | 此效果指定的屬性。None 表示欄位沒有指定一般五屬性，不等於已證明是「無屬性攻擊」。 |
| Power | float? | 主要效果強度。可能是倍率、百分比或其他係數，須配合 SkillEffectType 判讀。 |
| PowerFixed | float? | 固定值成分；是否與 Power 相加及運算順序要依效果類型確認。 |
| Probability | int | 觸發／成功機率的原始整數值。常見資料可能以百分比表達，但比例仍應由實例或程式邏輯確認。 |
| EffectCount | int | 次數、段數、層數或可作用次數；意義依效果類型而變。 |
| EffectRange | SkillEffectRange | 目標範圍。 |
| EffectRangeMode | SkillEffectRangeMode | 友方範圍如何跨陣營判定。對 Self 等範圍通常沒有實際影響。 |
| EffectRangeFlags | int? | 當範圍為 AttributeWeaponRarityParty／Enemy 時，用位元旗標指定星級、武器或屬性條件。 |
| EffectDuration | int? | 持續值；必須與 SkillEffectDurationMode 一起讀，不能只看數字就認定為回合。 |
| SkillEffectDurationMode | SkillEffectDurationModes? | 持續值的單位／消耗方式。0 是有效值 Turn，不是「沒有提供」。 |
| AdditionalPowerCondition | SkillEffectTypes? | 額外威力生效時所要求的效果種類。具體判定仍依使用此欄位的邏輯。 |
| AdditionalPower | int? | 額外威力值；如何加入主威力取決於效果類型。 |
| SkillEffectResourceName | string | 效果用資源名稱，例如演出或特效資源；null 表示未指定。 |
| EffectFlags | int | 額外行為旗標。沒有通用對照表，必須依 SkillEffectType 選擇正確的旗標家族。 |
| IconResourceName | string | 狀態圖示資源名稱。 |
| CustomDescription | string | 自訂效果說明。 |
| IconFlags | SkillEffectIconFlags | 圖示顯示方式。 |
| ModificationGroupId | int? | 效果修改群組 ID；可能用於同組效果的覆蓋、合併或限制，但精確規則尚未由 dump.cs 證明。 |

Power、PowerFixed、Probability、EffectCount、EffectDuration、AdditionalPower 與 ModificationGroupId 都是一般數值，不是「每個整數各代表一種效果」的 enum。它們必須依 SkillEffectType、相關模式與父技能資料解讀。

## SkillEffectType

### 1–19：基本傷害、回復、能力與異常

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 1 | Damage | 造成傷害。 |
| 2 | Healing | HP 回復。 |
| 3 | MaxHPEffect | 最大 HP 變化。 |
| 4 | AttackPowerEffect | 攻擊力變化。 |
| 5 | DefenceEffect | 防禦力變化。 |
| 6 | MagicalAttackPowerEffect | 魔法攻擊力變化。 |
| 7 | HealingPowerEffect | 回復力變化。 |
| 8 | SpeedEffect | 速度變化。 |
| 9 | CriticalStrikeChanceEffect | 暴擊率變化。 |
| 10 | CooltimeLeft | 剩餘 CT 變化。 |
| 11 | PoisonEffect | 毒效果。 |
| 12 | ParalysisControlEffect | 麻痺相關控制／耐性效果。 |
| 13 | ConfusionControlEffect | 混亂相關控制／耐性效果。 |
| 14 | EnchantedControlEffect | 幻惑相關控制／耐性效果。客戶端名稱是 Enchanted。 |
| 15 | CurseControlEffect | 詛咒相關控制／耐性效果。 |
| 16 | SealControlEffect | 封印相關控制／耐性效果。 |
| 17 | StunControlEffect | 暈眩相關控制／耐性效果。 |
| 18 | SleepControlEffect | 睡眠相關控制／耐性效果。 |
| 19 | AllControlEffects | 全部控制異常相關效果。 |

### 20–39：獎勵、CT、Buff 與連鎖技能

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 20 | UserExperienceBonus | 玩家經驗值加成。 |
| 21 | MonsterExperienceBonus | 角色／怪物經驗值加成。 |
| 22 | MoneyBonus | 金錢獲得量加成。 |
| 23 | ItemDropchanceBonus | 道具掉落率加成。 |
| 24 | CooltimeSpeedMultiplierEffect | CT 速度倍率變化。 |
| 25 | ResistanceEffect | 耐性變化；具體對象要看相關條件或父技能。 |
| 26 | LifeLeech | 吸血／傷害轉 HP。 |
| 27 | AllBuffs | 全部 Buff 的整體操作。 |
| 28 | Recovery | 回復／解除類效果；確切對象依技能資料。 |
| 29 | AdditionalLoot | 額外掉落。 |
| 30 | Buffs | Buff 操作。 |
| 31 | Intervention | 介入／援護類效果；精確戰鬥行為需查程式邏輯。 |
| 32 | Threatening | 威嚇／仇恨目標相關效果。 |
| 33 | CheatDeath | 免死／承受致命傷時存活。 |
| 34 | Dodge | 迴避。 |
| 35 | ChainSkillExtraPower | 連鎖技能額外威力。 |
| 36 | TurnStartCooltimeLeft | 回合開始時的剩餘 CT 變化。 |
| 37 | ExtraPowerMultiplier | 額外威力倍率。 |
| 38 | NativeSkillAssistance | 固有技能援護／協助發動。 |
| 39 | ChainSkillExtraPoints | 連鎖技能額外點數。 |

### 40–59：反擊、反射、追加攻擊與特殊強化

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 40 | Retaliation | 反擊。 |
| 41 | CooltimePenaltyModifier | CT 懲罰修正。 |
| 42 | SublimateSkill | 技能昇華／變化。 |
| 43 | SelfExplosion | 自爆。 |
| 44 | Multistrike | 多重攻擊。 |
| 45 | DamageReflection | 傷害反射。 |
| 46 | ExtraAttack | 追加攻擊。 |
| 47 | AuraPowerLimitBreak | Aura 威力上下限突破。 |
| 48 | AmplifyFood | 食物效果增幅。 |
| 49 | Buffsteal | 偷取 Buff。 |
| 50 | StealItem | 偷取道具。 |
| 51 | CooltimeLeftWeakness | 弱點相關的剩餘 CT 效果；精確觸發條件需查邏輯。 |
| 52 | CriticalDamage | 暴擊傷害變化。 |
| 53 | AllDebuffs | 全部 Debuff 的整體操作。 |
| 54 | Debuffs | Debuff 操作。 |
| 55 | ChangeDamageAttribute | 改變傷害屬性。 |
| 56 | BonusEventPoints | 活動點數加成。 |
| 57 | PartDestructionBonus | 部位破壞加成。 |
| 58 | AdditionalPower | 追加威力。 |
| 59 | DamageReflectionPenetration | 傷害反射貫通。通常表示讓相符類型的攻擊繞過反射，但不等於解除敵方反射，也不自動代表無視防禦、護盾或吸收。 |

### 60 以後

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 60 | ChainSkillPointsModification | 連鎖技能點數修正。 |
| 61 | StealItemPower | 偷取道具能力／強度。 |
| 62 | DummyCounter | Dummy 計數器；用途需依呼叫端確認。 |
| 63 | TransferDebuff | 轉移 Debuff。 |
| 64 | DestroyPart | 破壞部位。 |
| 65 | DamageMultiplier | 傷害倍率。 |
| 66 | TriggerAura | 觸發 Aura。 |
| 67 | Resurrect | 復活。 |
| 68–69 | 未定義 | 目前客戶端 enum 沒有定義。 |
| 70 | ForceMutationAdditionalPower | 強制技能變化時的追加威力。 |
| 71 | CopyBuffs | 複製 Buff。 |
| 72–75 | 未定義 | 目前客戶端 enum 沒有定義。 |
| 76 | Barrier | 屏障。 |
| 77–78 | 未定義 | 目前客戶端 enum 沒有定義。 |
| 79 | Provocation | 挑釁／引導攻擊目標。 |
| 80 | FieldBuff | 場地 Buff。 |
| 81 | HpAdjustment | HP 調整。 |
| 82–85 | 未定義 | 目前客戶端 enum 沒有定義。 |
| 86 | Accumulation | 累積／蓄積效果。 |

## SkillEffectModifier

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 1 | Increase | 增加／上升。實際用語應與效果種類合併，例如 AttackPowerEffect + Increase = 攻擊力上升。 |
| 2 | Decrease | 減少／下降。 |
| 3 | ResistanceIncrease | 對該效果的耐性上升。 |
| 4 | ResistanceDecrease | 對該效果的耐性下降。 |

Modifier 只表示方向，不足以單獨判斷效果。例如 Damage + Increase、PoisonEffect + ResistanceIncrease 和 CooltimeLeft + Decrease 的自然語意都不同。

## Attribute

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 1 | Fire | 火。 |
| 2 | Water | 水。 |
| 3 | Tree | 樹。 |
| 4 | Light | 光。 |
| 5 | Darkness | 闇。 |
| 6 | None | 未指定一般屬性。不能僅憑此值認定攻擊一定是無屬性。 |
| 7 | Special | 特殊屬性。 |

## EffectRange

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 1 | EnemyOne | 單一敵人。 |
| 2 | EnemyAll | 全體敵人。 |
| 3 | EnemyMultipleRandom | 隨機多名敵人。 |
| 4 | FriendOne | 單一友方。 |
| 5 | FriendAll | 全體友方。 |
| 6 | FriendMultipleRandom | 隨機多名友方。 |
| 7 | Self | 自己。 |
| 8 | FriendExceptSelf | 自己以外的友方。 |
| 9 | EveryoneExceptSelf | 自己以外的所有人。 |
| 10 | Everyone | 所有人。 |
| 11 | FireAttributeFriend | 火屬性友方。 |
| 12 | WaterAttributeFriend | 水屬性友方。 |
| 13 | TreeAttributeFriend | 樹屬性友方。 |
| 14 | LightAttributeFriend | 光屬性友方。 |
| 15 | DarknessAttributeFriend | 闇屬性友方。 |
| 16 | PartyAll | 全隊。 |
| 17 | PartyAllExceptSelf | 自己以外的全隊。 |
| 18 | FireAttributeEnemy | 火屬性敵人。 |
| 19 | WaterAttributeEnemy | 水屬性敵人。 |
| 20 | TreeAttributeEnemy | 樹屬性敵人。 |
| 21 | LightAttributeEnemy | 光屬性敵人。 |
| 22 | DarknessAttributeEnemy | 闇屬性敵人。 |
| 23 | ActionContext | 當前動作上下文所指定的目標。 |
| 24 | AttributeWeaponRarityParty | 依屬性、武器種類、稀有度篩選我方隊伍；條件在 EffectRangeFlags。 |
| 25 | AttributeWeaponRarityEnemy | 依屬性、武器種類、稀有度篩選敵方；條件在 EffectRangeFlags。 |
| 26 | NoAttributeEnemy | 不符合指定屬性的敵人／無指定屬性敵人；精確條件需查實作。 |
| 27 | BossFriend | BOSS 方友軍。 |
| 28 | FriendExceptSummoned | 召喚單位以外的友方。 |
| 29 | Spirit | 精靈。 |

## EffectRangeMode

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | OnlySameSideFriends | 只把同一陣營視為友方。 |
| 1 | BothSidesFriends | 兩個陣營都按友方範圍處理。 |

此欄位要與 EffectRange 一起讀。當 EffectRange = 7（Self）時，EffectRangeMode 通常不改變目標。

## EffectRangeFlags

當 EffectRange = 24 或 25 時，EffectRangeFlags 使用 EffectRangeAttributeWeaponRarityFlags。這是 [Flags] 位元集合，可同時指定多個條件。

| 位元值 | 客戶端名稱 | 條件 |
|---:|---|---|
| 0 | NoFlags | 沒有旗標。 |
| 1 | Star1 | ★1。 |
| 2 | Star2 | ★2。 |
| 4 | Star3 | ★3。 |
| 8 | Star4 | ★4。 |
| 16 | Star5 | ★5。 |
| 32 | Sword | 劍。 |
| 64 | Axe | 斧。 |
| 128 | Spear | 槍。 |
| 256 | Book | 本。 |
| 512 | Wand | 杖。 |
| 1024 | Dagger | 短劍。 |
| 2048 | Bow | 弓。 |
| 4096 | Special | 特殊武器。 |
| 8192 | Fire | 火屬性。 |
| 16384 | Water | 水屬性。 |
| 32768 | Tree | 樹屬性。 |
| 65536 | Light | 光屬性。 |
| 131072 | Darkness | 闇屬性。 |

例如 8224 = 8192 + 32，表示 Fire 與 Sword 兩個旗標同時存在。旗標之間是「聯集」還是要同時滿足，仍要看範圍篩選的實作，不能只靠數值表推定。

## SkillEffectDurationMode

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | Turn | 以回合計。 |
| 1 | Action | 以行動次數計。 |
| 2 | DamageTaken | 以承受傷害次數計。 |
| 3 | Charge | 以蓄力／充能次數計。 |
| 4 | DuringSkillExecution | 只在該技能執行期間有效。 |

例：EffectDuration = 1 只代表「持續值 1」。若 SkillEffectDurationMode 沒有出現在資料裡，不能直接寫成「持續 1 回合」。

## IconFlags

SkillEffectIconFlags 在 dump.cs 上沒有標出 [Flags] 屬性，但名稱與 1、2、4、8 的值排列呈位元旗標形式。遇到組合值時可先按位拆解，再以 UI 實際顯示確認。

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無特殊圖示行為。 |
| 1 | InvertVisibility | 反轉可見性。 |
| 2 | ShowAppliedEffectsCount | 顯示已套用的效果數量。 |
| 4 | MultipleEffectAura | 多效果 Aura 圖示。 |
| 8 | NoLimitEffect | 無上限效果的圖示行為。 |

可能的組合例：

- 3 = InvertVisibility + ShowAppliedEffectsCount
- 6 = ShowAppliedEffectsCount + MultipleEffectAura
- 10 = ShowAppliedEffectsCount + NoLimitEffect

## EffectFlags

EffectFlags 沒有一張可套用到所有技能的通用表。同一個數字在不同 SkillEffectType 下可能代表完全不同的行為；必須先確認效果種類，再選擇對應的旗標家族。

### CooltimeLeftEffectFlags

用於 CT 剩餘量相關效果。

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | TargetRecentSkill | 以最近使用的技能為目標。 |
| 2 | ApplyAsAura | 以 Aura 方式套用。 |
| 4 | TargetCurrentSkill | 以目前技能為目標。 |

### DamageEffectFlags

用於 Damage 類效果。

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | IgnoreDamageResistance | 無視傷害耐性。 |
| 2 | HpPercentDamage | 依 HP 百分比造成傷害。 |
| 4 | UseDefenceStatusInFormula | 傷害公式使用防禦狀態值。 |
| 8 | UseHealStatusInFormula | 傷害公式使用回復狀態值。 |
| 16 | UseHpStatusInFormula | 傷害公式使用 HP 狀態值。 |
| 32 | UseMagicStatusInFormula | 傷害公式使用魔攻狀態值。 |
| 64 | UseSpeedStatusInFormula | 傷害公式使用速度狀態值。 |
| 128 | UseLeaderAttribute | 使用隊長屬性。 |
| 256 | IgnoreAttributeAffinity | 無視屬性相剋。 |
| 512 | IgnoreCriticalStrike | 不進行／無視暴擊判定。 |
| 1024 | IgnorePowerMultiplier | 無視威力倍率。 |

### ExtraPowerEffectFlags

用於額外威力倍率等條件。

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | EffectTypeConditionIncludeDamage | 效果種類條件包含傷害。 |
| 2 | EffectTypeConditionIncludeHealing | 效果種類條件包含回復。 |
| 4 | Reserved1 | 保留位元 1，尚無可確認語意。 |
| 8 | Reserved2 | 保留位元 2，尚無可確認語意。 |
| 16 | SkillTypeConditionIncludeAttack | 技能類別包含攻擊。 |
| 32 | SkillTypeConditionIncludeSupport | 技能類別包含輔助。 |
| 64 | SkillTypeConditionIncludeAttackMagical | 技能類別包含魔法攻擊。 |
| 128 | SkillTypeConditionIncludeSupportMagical | 技能類別包含魔法輔助。 |

### NativeSkillAssistanceEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | OnlyNativeSkill | 只限固有技能。 |
| 2 | SkillTypeConditionIncludeAttack | 包含攻擊技能。 |
| 4 | SkillTypeConditionIncludeSupport | 包含輔助技能。 |
| 8 | SkillTypeConditionIncludeAttackMagical | 包含魔法攻擊技能。 |
| 16 | SkillTypeConditionIncludeSupportMagical | 包含魔法輔助技能。 |

### RetaliationEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | UseNativeSkill | 反擊使用固有技能。 |
| 2 | RetaliateNormalAttack | 對普通攻擊反擊。 |
| 4 | RetaliateSkillAttack | 對技能攻擊反擊。 |

### DamageReflectionEffectFlags

用於指定傷害反射或反射貫通所涵蓋的技能類別。

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | SkillTypeConditionIncludeAttack | 包含攻擊技能。 |
| 2 | SkillTypeConditionIncludeSupport | 包含輔助技能。 |
| 4 | SkillTypeConditionIncludeAttackMagical | 包含魔法攻擊技能。 |
| 8 | SkillTypeConditionIncludeSupportMagical | 包含魔法輔助技能。 |

### AuraPowerLimitBreakEffectFlags

| 數值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | AffectLowerLimit | 影響下限。 |
| 2 | AffectUpplerLimit | 影響上限。客戶端名稱中的 Uppler 應是 Upper 的拼字錯誤。 |
| 3 | AffectBothLimits | 同時影響上下限，即 1 + 2。 |

### SublimateSkillEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | ForceMutation | 強制技能變化。 |

### BuffsDebuffsEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | StatusEffects | 包含狀態異常效果。 |

### AdditionalLootEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | ModifyRareLootProbability | 修改稀有掉落機率。 |
| 2 | PartsLoot | 部位掉落。 |

### AdditionalPowerEffectFlags

| 位元值 | 客戶端名稱 | 中文意義 |
|---:|---|---|
| 0 | None | 無。 |
| 1 | SkillTypeConditionIncludeAttack | 包含攻擊技能。 |
| 2 | SkillTypeConditionIncludeSupport | 包含輔助技能。 |
| 4 | SkillTypeConditionIncludeAttackMagical | 包含魔法攻擊技能。 |
| 8 | SkillTypeConditionIncludeSupportMagical | 包含魔法輔助技能。 |

### 旗標組合範例

若某筆 Damage 的 EffectFlags = 5：

- 5 = 1 + 4
- 1 = IgnoreDamageResistance
- 4 = UseDefenceStatusInFormula

因此它同時帶有「無視傷害耐性」與「公式使用防禦狀態值」兩個旗標。不能把 5 當成另一個獨立、未列出的效果。

## 範例：Id 739023

原始資料：

    {
      "Id": 739023,
      "Order": 8,
      "SkillEffectType": 59,
      "SkillEffectModifier": 1,
      "Attribute": 6,
      "Power": 100.0,
      "PowerFixed": null,
      "EffectRange": 7,
      "EffectRangeMode": 0,
      "EffectDuration": 1,
      "SkillEffectResourceName": null,
      "IconResourceName": null,
      "CustomDescription": null,
      "IconFlags": 0
    }

逐欄解析：

| 欄位 | 數值 | 解讀 |
|---|---:|---|
| Id | 739023 | 這筆效果的 ID。 |
| Order | 8 | 在父技能的效果列表中排序為 8。 |
| SkillEffectType | 59 | DamageReflectionPenetration，傷害反射貫通。 |
| SkillEffectModifier | 1 | Increase，增加此貫通效果。 |
| Attribute | 6 | None，效果欄位未指定五大屬性；不代表父技能一定是無屬性攻擊。 |
| Power | 100.0 | 此效果的強度值為 100。它不是「傷害 100%」；是否代表 100% 反射貫通，仍需以同類技能資料或 Build.wasm／實戰驗證。 |
| PowerFixed | null | 沒有提供固定值成分。 |
| EffectRange | 7 | Self，只套用自己。 |
| EffectRangeMode | 0 | OnlySameSideFriends；由於目標是 Self，通常不改變結果。 |
| EffectDuration | 1 | 持續值為 1。資料未提供 SkillEffectDurationMode，所以不能確定是 1 回合、1 次行動、1 次受傷或其他模式。 |
| SkillEffectResourceName | null | 沒有指定額外效果資源。 |
| IconResourceName | null | 沒有指定圖示資源。 |
| CustomDescription | null | 沒有自訂描述。 |
| IconFlags | 0 | None，無特殊圖示行為。 |

較安全的整體描述是：

> 對自身套用強度值 100 的「傷害反射貫通」效果。它通常用來讓相符技能類別繞過傷害反射，但這筆資料本身不能證明它會解除反射、無視防禦、貫穿屏障／吸收，也不能在缺少 DurationMode 時判定持續 1 回合。

若完整物件還有 EffectFlags，應按 DamageReflectionEffectFlags 拆解，才能確認它涵蓋攻擊、輔助、魔法攻擊或魔法輔助中的哪些技能類別。
