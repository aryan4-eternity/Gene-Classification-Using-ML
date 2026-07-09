import pandas as pd
import matplotlib.pyplot as plt
import re
import pathlib

DATA = ["data/human_data.txt", "data/chimp_data.txt"]

def clean_sequence(s):
    return re.sub(r"[^ACGT]", "", (s or "").upper())

def load(paths):
    frames = []
    for p in paths:
        df = pd.read_csv(p, sep=None, engine="python")
        df["sequence"] = df["sequence"].map(clean_sequence)
        df = df[df["sequence"].str.len() > 0]
        df["class"] = df["class"].astype(int)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

def gc_content(seq):
    return (seq.count('G') + seq.count('C')) / len(seq) * 100 if len(seq) > 0 else 0

df = load(DATA)
human_size = len(pd.read_csv(DATA[0], sep=None, engine="python"))
df['organism'] = ['Human' if i < human_size else 'Chimp' for i in range(len(df))]
df['length'] = df['sequence'].str.len()
df['gc'] = df['sequence'].apply(gc_content)

pathlib.Path('plots').mkdir(exist_ok=True)

# PLOT 1: Count
plt.figure(figsize=(10, 6))
df['organism'].value_counts().plot(kind='bar', color=['#FF6B6B', '#4ECDC4'])
plt.title('Human vs Chimp Sequences', fontsize=12, fontweight='bold')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('plots/01_count.png', dpi=300)
plt.close()

# PLOT 2: Gene Classes
plt.figure(figsize=(12, 6))
pd.crosstab(df['organism'], df['class']).plot(kind='bar', width=0.8)
plt.title('Gene Classes by Organism', fontsize=12, fontweight='bold')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('plots/02_classes.png', dpi=300)
plt.close()

# PLOT 3: Sequence Length
plt.figure(figsize=(12, 6))
plt.hist([df[df['organism']=='Human']['length'], df[df['organism']=='Chimp']['length']], 
         label=['Human', 'Chimp'], bins=20, color=['#FF6B6B', '#4ECDC4'])
plt.title('Sequence Length Distribution', fontsize=12, fontweight='bold')
plt.xlabel('Length (bp)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/03_length.png', dpi=300)
plt.close()

# PLOT 4: GC Content
plt.figure(figsize=(12, 6))
plt.hist([df[df['organism']=='Human']['gc'], df[df['organism']=='Chimp']['gc']], 
         label=['Human', 'Chimp'], bins=15, color=['#FF6B6B', '#4ECDC4'])
plt.title('GC Content Distribution', fontsize=12, fontweight='bold')
plt.xlabel('GC %')
plt.legend()
plt.tight_layout()
plt.savefig('plots/04_gc.png', dpi=300)
plt.close()

# PLOT 5: Scatter (GC vs Length)
plt.figure(figsize=(12, 6))
human = df[df['organism']=='Human']
chimp = df[df['organism']=='Chimp']
plt.scatter(human['length'], human['gc'], label='Human', alpha=0.6, color='#FF6B6B', s=50)
plt.scatter(chimp['length'], chimp['gc'], label='Chimp', alpha=0.6, color='#4ECDC4', s=50)
plt.title('GC Content vs Sequence Length', fontsize=12, fontweight='bold')
plt.xlabel('Length (bp)')
plt.ylabel('GC %')
plt.legend()
plt.tight_layout()
plt.savefig('plots/05_scatter.png', dpi=300)
plt.close()

# Summary
print("\n" + "="*60)
print("EDA SUMMARY")
print("="*60)
print(f"Total: {len(df)}")
print(f"Human: {len(df[df['organism']=='Human'])}")
print(f"Chimp: {len(df[df['organism']=='Chimp'])}")
print(f"Classes: {sorted(df['class'].unique())}")
print(f"\nLength (bp): min={df['length'].min()}, max={df['length'].max()}, mean={df['length'].mean():.1f}")
print(f"GC (%): min={df['gc'].min():.1f}, max={df['gc'].max():.1f}, mean={df['gc'].mean():.1f}")
print(f"\n✅ 5 plots saved in ./plots/")
print("="*60)