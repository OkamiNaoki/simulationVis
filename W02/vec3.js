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
    return Math.sqrt(
        (Math.pow(v0.x - v1.x, 2) + Math.pow(v0.y - v1.y, 2) + Math.pow(v0.z - v1.z, 2)) *
        (Math.pow(v0.x - v2.x, 2) + Math.pow(v0.y - v2.y, 2) + Math.pow(v0.z - v2.z, 2)) -
        (Math.pow(v0.x - v1.x, 2) + Math.pow(v0.y - v1.y, 2) + Math.pow(v0.z - v1.z, 2)) *
        (Math.pow(v0.x - v2.x, 2) + Math.pow(v0.y - v2.y, 2) + Math.pow(v0.z - v2.z, 2))
      ) / 2;
 }

  