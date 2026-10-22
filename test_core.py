import random,unittest
from rle_mask_topology import analyze

def rle(rows):
    h=len(rows);w=len(rows[0]);counts=[0];bit=0
    for x in range(w):
        for y in range(h):
            if rows[y][x]!=bit:counts.append(0);bit^=1
            counts[-1]+=1
    return {'size':[h,w],'counts':counts}
def groups(cells,neighbors):
    cells=set(cells);out=[]
    while cells:
        todo=[cells.pop()];group=set(todo)
        while todo:
            x,y=todo.pop()
            for dx,dy in neighbors:
                p=(x+dx,y+dy)
                if p in cells:cells.remove(p);todo.append(p);group.add(p)
        out.append(group)
    return out

class Masks(unittest.TestCase):
    def test_seeded_pixel_set_oracle(self):
        rng=random.Random(22);four=[(1,0),(-1,0),(0,1),(0,-1)];eight=[(a,b)for a in(-1,0,1)for b in(-1,0,1)if(a,b)!=(0,0)]
        for _ in range(50):
            h=rng.randrange(1,9);w=rng.randrange(1,9);rows=[[rng.randrange(2)for x in range(w)]for y in range(h)]
            fg={(x,y)for y in range(h)for x in range(w)if rows[y][x]};bg={(x,y)for y in range(h)for x in range(w)}-fg
            cs=groups(fg,four);holes=sum(all(0<x<w-1 and 0<y<h-1 for x,y in g)for g in groups(bg,eight));r=analyze(rle(rows))
            self.assertEqual(r['area'],len(fg));self.assertEqual(r['component_count'],len(cs));self.assertEqual(r['holes'],holes)
            self.assertEqual(r['perimeter'],sum((x+dx,y+dy)not in fg for x,y in fg for dx,dy in four))
            self.assertEqual(sorted(c['area']for c in r['components']),sorted(map(len,cs)))
    def test_ring_hole_and_bounding_box(self):
        r=analyze(rle([[1,1,1],[1,0,1],[1,1,1]]));self.assertEqual((r['area'],r['holes'],r['perimeter'],r['euler_characteristic']),(8,1,16,0));self.assertEqual(r['components'][0]['bbox'],[0,0,3,3])
    def test_diagonal_connectivity_and_column_major(self):
        r=analyze({'size':[2,3],'counts':[0,1,2,1,2]});self.assertEqual(r['component_count'],2);self.assertEqual([c['bbox']for c in r['components']],[[0,0,1,1],[1,1,1,1]])
        r=analyze(rle([[0,1,1],[1,0,1],[1,1,1]]));self.assertEqual(r['holes'],0)
    def test_empty_full_and_zero_length_runs(self):
        self.assertEqual(analyze({'size':[2,2],'counts':[4]})['area'],0)
        self.assertEqual(analyze({'size':[2,2],'counts':[0,4]})['perimeter'],8)
        self.assertEqual(analyze({'size':[1,1],'counts':[0,0,0,1]})['area'],1)
    def test_reject_invalid_runs_and_shape(self):
        for d in [{'size':[2,2],'counts':[3]},{'size':[2,2],'counts':'compressed'},{'size':[0,2],'counts':[]},{'size':[1,1],'counts':[True]},{'size':[1,1],'counts':[-1,2]}]:
            with self.assertRaises(ValueError):analyze(d)

if __name__=='__main__':unittest.main()
