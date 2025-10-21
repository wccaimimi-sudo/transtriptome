#/data1/wcc/transcriptome/5.counts
import pandas as pd
import argparse
import sys

def counts_to_tpm(counts_df):
    """Converts a raw count matrix from featureCounts to TPM."""
    # featureCounts的输出中，'Length'列是计算TPM的关键
    if 'Length' not in counts_df.columns:
        sys.exit("Error: 'Length' column not found in the input file. This is required for TPM calculation.")
        gene_lengths = counts_df['Length']
     # 提取所有样本的原始计数值（从第7列开始）
    raw_counts = counts_df.iloc[:, 6:]
     # 1. 计算 RPK (Reads Per Kilobase)
    # RPK = (Read Counts) / (Gene Length in kb)
    rpk = raw_counts.div(gene_lengths / 1000, axis=0)
    
    # 2. 计算每个样本的 "Per Million" 缩放因子
    # Scaling Factor = Sum of all RPK values in a sample / 1,000,000
    scaling_factor = rpk.sum() / 1_000_000
    
    # 3. 计算 TPM
    # TPM = RPK / Scaling Factor
    tpm = rpk.div(scaling_factor, axis=1)
    
    # 将基因ID列重新加回去
    tpm.insert(0, 'Geneid', counts_df['Geneid'])
    
    return tpm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert featureCounts raw counts to TPM.")
    parser.add_argument("-i", "--input", required=True, help="Input featureCounts file (raw counts).")
    parser.add_argument("-o", "--output", required=True, help="Output TPM file path.")
    args = parser.parse_args()

    try:
        # 加载featureCounts的输出，跳过可能存在的第一行注释
        counts_df = pd.read_csv(args.input, sep='\t', comment='#')
        
        print(f"Successfully loaded {len(counts_df)} genes from {args.input}")
        
        tpm_df = counts_to_tpm(counts_df)
        
        tpm_df.to_csv(args.output, sep='\t', index=False, float_format='%.4f')
        
        print(f"TPM matrix with {tpm_df.shape[0]} genes and {tpm_df.shape[1]-1} samples saved to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
