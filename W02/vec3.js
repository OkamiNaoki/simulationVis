function Vec3(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
  
  Vec3.prototype.min = function() {
    if (this.x < this.y) {
      if (this.x < this.z) {
        return this.x;
      } else {
        return this.z;
      }
    } else if (this.y < this.z) {
      return this.y;
    } else {
      return this.z;
    }
  };
  
  Vec3.prototype.mid = function() {
    if (this.x < this.y) {
      if (this.x > this.z) {
        return this.x;
      } else if (this.y < this.z) {
        return this.y;
      } else {
        return this.z;
      }
    } else if (this.y > this.z) {
      return this.y;
    } else if (this.x < this.z) {
      return this.x;
    } else {
      return this.z;
    }
  }
  
  Vec3.prototype.max = function() {
    if (this.x < this.y) {
      if (this.y < this.z) {
        return this.z;
      } else {
        return this.y;
      }
    } else if (this.x < this.z) {
      return this.z;
    } else {
      return this.x;
    }
  }

  function AreaOfTriangle( v0, v1, v2 ) {
    // 3つの辺の長さを計算
    var a = Math.sqrt(Math.pow(v1.x - v0.x, 2) + Math.pow(v1.y - v0.y, 2) + Math.pow(v1.z - v0.z, 2));
    var b = Math.sqrt(Math.pow(v2.x - v1.x, 2) + Math.pow(v2.y - v1.y, 2) + Math.pow(v2.z - v1.z, 2));
    var c = Math.sqrt(Math.pow(v0.x - v2.x, 2) + Math.pow(v0.y - v2.y, 2) + Math.pow(v0.z - v2.z, 2));
    var s = (a + b + c) / 2;
    var area = Math.sqrt(s * (s - a) * (s - b) * (s - c));
    return area;
}

  