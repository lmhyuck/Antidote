import re
from typing import List, Dict

class TextProcessor:
    def __init__(self):
        self.struct_pattern = r'(제\s*\d+\s*조(?:\s*\(.*?\))?|①|②|③|④|⑤|\d+\.)'

    def clean_for_embedding(self, text: str) -> str:
        clean_text = re.sub(self.struct_pattern, '', text)
        clean_text = re.sub(r'[^\w\s.가-힣]', ' ', clean_text)
        return " ".join(clean_text.split()).strip()

    def smart_chunking(self, text: str) -> List[Dict[str, str]]:
        # [중요] 연속 공백만 제거하고 \n(줄바꿈)은 절대 건드리지 마세요!
        processed_text = re.sub(r' +', ' ', text).strip()
        
        combined_chunks = []
        
        matches = list(re.finditer(self.struct_pattern, processed_text))
        
        if matches:
            for i in range(len(matches)):
                start_pos = matches[i].start()
                # 다음 조항의 시작 전까지가 현재 조항의 내용입니다.
                end_pos = matches[i+1].start() if i + 1 < len(matches) else len(processed_text)
                
                full_clause = processed_text[start_pos:end_pos].strip()
                
                if len(full_clause) > 5:
                    combined_chunks.append(full_clause)
        else:
            # 조항 형식이 전혀 없을 때만 기존 마침표 분리 사용
            combined_chunks = [s.strip() + "." for s in processed_text.split('. ') if len(s.strip()) > 5]

        return [{"original": c, "for_embedding": self.clean_for_embedding(c)} for c in combined_chunks]
    def clean_pdf_text(self, text_input) -> str:
        if isinstance(text_input, list):
            text = "\n".join(map(str, text_input))
        else:
            text = str(text_input)

        # 조항 번호 앞에 줄바꿈 강제 (smart_chunking이 잘 자를 수 있게)
        text = re.sub(r'([^\n])\s*(\d+\.)(?=\s|$)', r'\1\n\2', text)
        text = re.sub(r'([^\n])\s*(제\s*\d+\s*조)', r'\1\n\2', text)

        # 불필요한 연속 공백 정제 (줄바꿈 \n은 건드리지 않음)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n+', '\n', text) # 연속된 줄바꿈만 하나로 합침
        
        return text.strip()