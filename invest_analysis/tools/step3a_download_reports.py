#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step3a: Financial Report Download Tool
从巨潮资讯(CNINFO)自动下载A股上市公司的年报和季报

使用方法:
    python step3a_download_reports.py --input ../step2/02_标的清单.yaml --output ../step3/financials

功能:
    1. 读取Step2生成的标的清单YAML文件
    2. 从巨潮资讯获取每家公司的最新年报和季报
    3. 按公司代码和名称组织到输出目录
    4. 生成下载日志和元数据
"""

import os
import sys
import yaml
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportDownloader:
    """财报下载器"""
    
    # CNINFO API 配置（示例，实际需要根据最新API调整）
    CNINFO_BASE_URL = "https://www.cninfo.com.cn/new/api"
    
    # 报告类型代码
    REPORT_TYPES = {
        "annual": "1",      # 年报
        "q1": "2",         # 一季报
        "q2": "3",         # 半年报
        "q3": "4",         # 三季报
    }
    
    def __init__(self, input_file: str, output_dir: str, skip_existing: bool = True):
        """
        初始化下载器
        
        Args:
            input_file: Step2的标的清单YAML文件路径
            output_dir: 输出目录路径
            skip_existing: 是否跳过已存在的文件
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.skip_existing = skip_existing
        self.stocks = []
        self.download_log = []
        
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_stock_list(self) -> bool:
        """
        加载标的清单
        
        Returns:
            bool: 是否成功加载
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.stocks = data if isinstance(data, list) else []
                logger.info(f"成功加载{len(self.stocks)}只股票")
                return True
        except Exception as e:
            logger.error(f"加载标的清单失败: {e}")
            return False
    
    def create_stock_directory(self, code: str, name: str) -> Path:
        """
        为每只股票创建目录
        
        Args:
            code: 股票代码
            name: 股票名称
            
        Returns:
            Path: 股票目录路径
        """
        stock_dir = self.output_dir / f"{code}_{name}"
        stock_dir.mkdir(parents=True, exist_ok=True)
        return stock_dir
    
    def download_report(self, code: str, name: str, report_type: str = "annual") -> Optional[str]:
        """
        下载单个报告
        
        Args:
            code: 股票代码（6位数字）
            name: 股票名称
            report_type: 报告类型（annual/q1/q2/q3）
            
        Returns:
            Optional[str]: 下载后的文件路径，失败返回None
        """
        stock_dir = self.create_stock_directory(code, name)
        
        # 这是示例实现，实际应该调用真实API或web爬取
        # 由于API可能变化，这里提供框架和注释
        
        logger.info(f"准备下载 {code}_{name} 的{self._get_report_type_name(report_type)}...")
        
        try:
            # 实现步骤:
            # 1. 调用CNINFO API或巨潮网站获取报告列表
            # 2. 找到最新的指定类型报告
            # 3. 下载PDF文件
            # 4. 保存到stock_dir
            
            # 示例：生成虚拟路径（实际开发需替换为真实下载）
            year = datetime.now().year
            filename = f"{year}_{report_type}_report.pdf"
            filepath = stock_dir / filename
            
            # TODO: 实现真实下载逻辑
            # 可选方案:
            # - 使用selenium + chromedriver 爬取巨潮网页
            # - 调用第三方数据API (如tushare, akshare等)
            # - 使用巨潮资讯的官方接口(如有)
            
            # 此处为占位符
            logger.info(f"[占位符] 将下载到: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"下载{code}_{name}的{report_type}报告失败: {e}")
            return None
    
    def download_all(self) -> Dict[str, List[str]]:
        """
        下载所有股票的报告
        
        Returns:
            Dict: 下载结果统计
        """
        results = {
            "success": [],
            "failed": [],
            "skipped": []
        }
        
        for stock in self.stocks:
            code = stock.get('code', '')
            name = stock.get('name', '')
            
            if not code or not name:
                logger.warning(f"跳过无效的股票: {stock}")
                continue
            
            # 为每种报告类型下载
            for report_type in ["annual", "q3", "q2", "q1"]:
                result = self.download_report(code, name, report_type)
                
                if result:
                    results["success"].append({
                        "code": code,
                        "name": name,
                        "type": report_type,
                        "path": result,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    results["failed"].append({
                        "code": code,
                        "name": name,
                        "type": report_type
                    })
        
        return results
    
    def save_metadata(self, results: Dict) -> None:
        """
        保存下载元数据
        
        Args:
            results: 下载结果字典
        """
        metadata_file = self.output_dir / "download_metadata.json"
        metadata = {
            "download_time": datetime.now().isoformat(),
            "total_stocks": len(self.stocks),
            "successful_downloads": len(results["success"]),
            "failed_downloads": len(results["failed"]),
            "results": results
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"元数据已保存到: {metadata_file}")
    
    def generate_report(self, results: Dict) -> None:
        """
        生成下载报告
        
        Args:
            results: 下载结果字典
        """
        report_file = self.output_dir / "step3a_download_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Step3a 财报下载报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**总股票数**: {len(self.stocks)}\n")
            f.write(f"**成功下载**: {len(results['success'])}\n")
            f.write(f"**下载失败**: {len(results['failed'])}\n\n")
            
            if results["success"]:
                f.write("## ✅ 成功下载的报告\n\n")
                for item in results["success"]:
                    f.write(f"- {item['code']}_{item['name']}: {item['type']} ({item['path']})\n")
            
            if results["failed"]:
                f.write("\n## ❌ 下载失败的报告\n\n")
                for item in results["failed"]:
                    f.write(f"- {item['code']}_{item['name']}: {item['type']}\n")
                f.write("\n**建议**: 检查网络连接，或手动从巨潮资讯下载这些报告\n")
        
        logger.info(f"下载报告已生成: {report_file}")
    
    @staticmethod
    def _get_report_type_name(report_type: str) -> str:
        """获取报告类型的中文名称"""
        names = {
            "annual": "年报",
            "q3": "三季报",
            "q2": "半年报",
            "q1": "一季报"
        }
        return names.get(report_type, report_type)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Step3a: 从巨潮资讯下载财报',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认路径
  python step3a_download_reports.py
  
  # 指定自定义路径
  python step3a_download_reports.py \\
    --input ../step2/02_标的清单.yaml \\
    --output ../step3/financials
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        default='../step2/02_标的清单.yaml',
        help='Step2标的清单YAML文件路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='../step3/financials',
        help='输出目录路径'
    )
    
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        default=True,
        help='是否跳过已存在的文件'
    )
    
    args = parser.parse_args()
    
    # 创建下载器并执行
    downloader = ReportDownloader(
        input_file=args.input,
        output_dir=args.output,
        skip_existing=args.skip_existing
    )
    
    if not downloader.load_stock_list():
        return 1
    
    results = downloader.download_all()
    downloader.save_metadata(results)
    downloader.generate_report(results)
    
    # 打印统计
    logger.info(f"========== 下载完成 ==========")
    logger.info(f"成功: {len(results['success'])}")
    logger.info(f"失败: {len(results['failed'])}")
    logger.info(f"==============================")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
